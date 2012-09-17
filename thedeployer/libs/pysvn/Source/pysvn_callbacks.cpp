//
// ====================================================================
// Copyright (c) 2003-2008 Barry A Scott.  All rights reserved.
//
// This software is licensed as described in the file LICENSE.txt,
// which you should have received as part of this distribution.
//
// ====================================================================
//
//
//  pysvn_callbacks.cpp
//
#if defined( _MSC_VER )
// disable warning C4786: symbol greater than 255 character,
// nessesary to ignore as <map> causes lots of warning
#pragma warning(disable: 4786)
#endif

#include "pysvn.hpp"

static bool get_string( Py::Object &fn, Py::Tuple &args, std::string & _msg );

pysvn_context::pysvn_context( const std::string &config_dir )
: SvnContext( config_dir )
, m_pyfn_GetLogin()
, m_pyfn_Notify()
#if defined( PYSVN_HAS_CONTEXT_PROGRESS )
, m_pyfn_Progress()
#endif
, m_pyfn_GetLogMessage()
, m_pyfn_SslServerPrompt()
, m_pyfn_SslServerTrustPrompt()
, m_pyfn_SslClientCertPrompt()
, m_pyfn_SslClientCertPwPrompt()
, m_permission( NULL )
, m_error_message()
, m_log_message()
{
}


pysvn_context::~pysvn_context()
{
}

bool pysvn_context::hasPermission()
{
    return m_permission != NULL;
}

void pysvn_context::setPermission( PythonAllowThreads &_permission )
{
    assert( m_permission == NULL );
    m_permission = &_permission;
    m_error_message = "";
}

void pysvn_context::clearPermission()
{
    m_permission = NULL;
}

void pysvn_context::checkForError( Py::ExtensionExceptionType &exception_for_error )
{
    // see if any errors occurred in the callbacks
    if( !m_error_message.empty() )
    {
        throw Py::Exception( exception_for_error, m_error_message );
    }
}

//
// this method will be called to retrieve
// authentication information
//
// WORKAROUND FOR apr_xlate PROBLEM: 
// STRINGS ALREADY HAVE TO BE UTF8!!!
//
// @retval true continue
//
bool pysvn_context::contextGetLogin
    (
    const std::string & _realm,
    std::string & _username, 
    std::string & _password,
    bool &_may_save
    )
{
    PythonDisallowThreads callback_permission( m_permission );

    // make sure we can call the users object
    if( !m_pyfn_GetLogin.isCallable() )
    {
        m_error_message = "callback_get_login required";
        return false;
    }

    Py::Callable callback( m_pyfn_GetLogin );

    Py::Tuple args( 3 );
    args[0] = Py::String( _realm );
    args[1] = Py::String( _username );
    args[2] = Py::Int( (long)_may_save );

    // bool, username, password
    Py::Tuple results;
    Py::Int retcode;
    Py::String username;
    Py::String password;
    Py::Int may_save_out;

    try
    {
        results = callback.apply( args );
        retcode = results[0];
        username = results[1];
        password = results[2];
        may_save_out = results[3];

        // true returned
        if( long( retcode ) != 0 )
        {
            // copy out the answers
            _username = username.as_std_string();
            _password = password.as_std_string();
            _may_save = long( may_save_out ) != 0;

            return true;
        }
    }
    catch( Py::Exception &e )
    {
        PyErr_Print();
        e.clear();

        m_error_message = "unhandled exception in callback_get_login";

        return false;
    }

    return false;
}

#if defined( PYSVN_HAS_CONTEXT_PROGRESS )
void pysvn_context::contextProgress
    (
    apr_off_t progress,
    apr_off_t total
    )
{
    PythonDisallowThreads callback_permission( m_permission );

    // make sure we can call the users object
    if( !m_pyfn_Progress.isCallable() )
        return;

    Py::Callable callback( m_pyfn_Progress );

    Py::Tuple args( 2 );
    // on some platforms apr_off_t is int64
    args[0] = Py::Int( static_cast<long int>( progress ) );
    args[1] = Py::Int( static_cast<long int>( total ) );

    Py::Object results;

    try
    {
        results = callback.apply( args );
    }
    catch( Py::Exception &e )
    {
        PyErr_Print();
        e.clear();

        m_error_message = "unhandled exception in callback_progress";
    }
}
#endif

// 
// this method will be called to notify about
// the progress of an ongoing action
//

#if defined( PYSVN_HAS_CONTEXT_NOTIFY2 )
void pysvn_context::contextNotify2
    (
    const svn_wc_notify_t *notify,
    apr_pool_t *pool
    )
{
    PythonDisallowThreads callback_permission( m_permission );

    // make sure we can call the users object
    if( !m_pyfn_Notify.isCallable() )
        return;

    Py::Callable callback( m_pyfn_Notify );

    Py::Tuple args( 1 );
    Py::Dict info;
    args[0] = info;

    info["path"] = Py::String( notify->path );
    info["action"] = toEnumValue( notify->action );
    info["kind"] = toEnumValue( notify->kind );
    if( notify->mime_type == NULL )
        info["mime_type"] = Py::Nothing();
    else
        info["mime_type"] = Py::String( notify->mime_type );
    info["content_state"] = toEnumValue( notify->content_state );
    info["prop_state"] = toEnumValue( notify->prop_state );
    info["revision"] = Py::asObject( new pysvn_revision( svn_opt_revision_number, 0, notify->revision ) );
    if( notify->err != NULL )
    {
        SvnException error( notify->err );
        info["error"] = error.pythonExceptionArg( 1 );
    }
    else
    {
        info["error"] = Py::None();
    }

    Py::Object results;

    try
    {
        results = callback.apply( args );
    }
    catch( Py::Exception &e )
    {
        PyErr_Print();
        e.clear();

        m_error_message = "unhandled exception in callback_notify";
    }
}
#else
void pysvn_context::contextNotify
    (
    const char *path,
    svn_wc_notify_action_t action,
    svn_node_kind_t kind,
    const char *mime_type,
    svn_wc_notify_state_t content_state,
    svn_wc_notify_state_t prop_state,
    svn_revnum_t revnum
    )
{
    PythonDisallowThreads callback_permission( m_permission );

    // make sure we can call the users object
    if( !m_pyfn_Notify.isCallable() )
        return;

    Py::Callable callback( m_pyfn_Notify );

    Py::Tuple args( 1 );
    Py::Dict info;
    args[0] = info;

    info["path"] = Py::String( path );
    info["action"] = toEnumValue( action );
    info["kind"] = toEnumValue( kind );
    if( mime_type == NULL )
        info["mime_type"] = Py::Nothing();
    else
        info["mime_type"] = Py::String( mime_type );
    info["content_state"] = toEnumValue( content_state );
    info["prop_state"] = toEnumValue( prop_state );
    info["revision"] = Py::asObject( new pysvn_revision( svn_opt_revision_number, 0, revnum ) );

    Py::Object results;

    try
    {
        results = callback.apply( args );
    }
    catch( Py::Exception &e )
    {
        PyErr_Print();
        e.clear();

        m_error_message = "unhandled exception in callback_notify";
    }
}
#endif

//
//    Return true to cancel a long running operation
//
bool pysvn_context::contextCancel()
{
    PythonDisallowThreads callback_permission( m_permission );

    // make sure we can call the users object
    if( !m_pyfn_Cancel.isCallable() )
        return false;

    Py::Callable callback( m_pyfn_Cancel );

    Py::Tuple args( 0 );

    // bool
    Py::Object result;

    Py::Int retcode;

    try
    {
        result = callback.apply( args );
        retcode = result;

        return long( retcode ) != 0;
    }
    catch( Py::Exception &e )
    {
        PyErr_Print();
        e.clear();

        m_error_message = "unhandled exception in callback_cancel";

        return false;
    }
}

void pysvn_context::setLogMessage( const std::string & a_msg )
{
    m_log_message = a_msg;
}

//
// this method will be called to retrieve
// a log message
//
bool pysvn_context::contextGetLogMessage( std::string & a_msg )
{
    if( !m_log_message.empty() )
    {
        a_msg = m_log_message;
        m_log_message.erase();

        return true;
    }

    PythonDisallowThreads callback_permission( m_permission );

    if( !m_pyfn_GetLogMessage.isCallable() )
    {
        m_error_message = "callback_get_log_message required";
        return false;
    }

    Py::Tuple args( 0 );
    try
    {
        return get_string( m_pyfn_GetLogMessage, args, a_msg );
    }
    catch( Py::Exception &e )
    {
        PyErr_Print();
        e.clear();

        m_error_message = "unhandled exception in callback_get_log_message";
    }

    return false;
}

//
// this method is called if there is ssl server
// information, that has to be confirmed by the user
//
// @param data 
// @return @a SslServerTrustAnswer
//
bool pysvn_context::contextSslServerTrustPrompt
        ( 
        const svn_auth_ssl_server_cert_info_t &info, 
        const std::string &realm,
        apr_uint32_t &a_accepted_failures,
        bool &accept_permanent
        )
{
    PythonDisallowThreads callback_permission( m_permission );

    // make sure we can call the users object
    if( !m_pyfn_SslServerTrustPrompt.isCallable() )
    {
        m_error_message = "callback_ssl_server_trust_prompt required";

        return false;
    }

    Py::Callable callback( m_pyfn_SslServerTrustPrompt );

    Py::Dict trust_info;
    trust_info[Py::String("failures")] = Py::Int( long( a_accepted_failures ) );
    trust_info[Py::String("hostname")] = Py::String( info.hostname );
    trust_info[Py::String("finger_print")] = Py::String( info.fingerprint );
    trust_info[Py::String("valid_from")] = Py::String( info.valid_from );
    trust_info[Py::String("valid_until")] = Py::String( info.valid_until );
    trust_info[Py::String("issuer_dname")] = Py::String( info.issuer_dname );
    trust_info[Py::String("realm")] = Py::String( realm );

    Py::Tuple args( 1 );
    args[0] = trust_info;

    Py::Tuple result_tuple;
    Py::Int retcode;
    Py::Int accepted_failures;
    Py::Int may_save;

    try
    {
        result_tuple = callback.apply( args );
        retcode = result_tuple[0];
        accepted_failures = result_tuple[1];
        may_save = result_tuple[2];

        a_accepted_failures = long( accepted_failures );
        if( long( retcode ) != 0 )
        {
            accept_permanent = long( may_save ) != 0;
            return true;
        }
        else
            return false;
    }
    catch( Py::Exception &e )
    {
        PyErr_Print();
        e.clear();

        m_error_message = "unhandled exception in callback_ssl_server_trust_prompt";
    }

    return false;
}

//
// this method is called to retrieve client side
// information
//
bool pysvn_context::contextSslClientCertPrompt( std::string &_cert_file, const std::string &_realm, bool &_may_save )
{
    PythonDisallowThreads callback_permission( m_permission );

    if( !m_pyfn_SslClientCertPrompt.isCallable() )
    {
        m_error_message = "callback_ssl_client_cert_prompt required";

        return false;
    }

    Py::Callable callback( m_pyfn_SslClientCertPrompt );

    Py::Tuple args( 2 );
    args[0] = Py::String( _realm );
    args[1] = Py::Int( _may_save );

    Py::Tuple results;
    Py::Int retcode;
    Py::String cert_file;
    Py::Int may_save_out;

    try
    {
        results = callback.apply( args );
        retcode = results[0];
        cert_file = results[1];
        may_save_out = results[2];

        if( long( retcode ) != 0 )
        {
            _cert_file = cert_file.as_std_string();
            _may_save = long( may_save_out ) != 0;

            return true;
        }
    }
    catch( Py::Exception &e )
    {
        PyErr_Print();
        e.clear();

        m_error_message = "unhandled exception in callback_ssl_client_cert_prompt";

        return false;
    }

    return false;
}

//
// this method is called to retrieve the password
// for the certificate
//
// @param password
//
bool pysvn_context::contextSslClientCertPwPrompt
    (
    std::string &_password, 
    const std::string &_realm,
    bool &_may_save
    )
{
    PythonDisallowThreads callback_permission( m_permission );

    // make sure we can call the users object
    if( !m_pyfn_SslClientCertPwPrompt.isCallable() )
    {
        m_error_message = "callback_ssl_client_cert_password_prompt required";

        return false;
    }

    Py::Callable callback( m_pyfn_SslClientCertPwPrompt );

    Py::Tuple args( 2 );
    args[0] = Py::String( _realm );
    args[1] = Py::Int( (long)_may_save );

    // bool, username, password
    Py::Tuple results;
    Py::Int retcode;
    Py::String username;
    Py::String password;
    Py::Int may_save_out;

    try
    {
        results = callback.apply( args );
        retcode = results[0];
        password = results[1];
        may_save_out = results[2];

        // true returned
        if( long( retcode ) != 0 )
        {
            // copy out the answers
            _password = password.as_std_string();
            _may_save = long( may_save_out ) != 0;

            return true;
        }
    }
    catch( Py::Exception &e )
    {
        PyErr_Print();
        e.clear();

        m_error_message = "unhandled exception in callback_ssl_client_cert_password_prompt";

        return false;
    }

    return false;
}

// common get a string implementation
static bool get_string( Py::Object &fn, Py::Tuple &args, std::string &msg )
{
    // make sure we can call the users object
    if( !fn.isCallable() )
        return false;

    Py::Callable callback( fn );

    Py::Tuple results;
    Py::Int retcode;
    Py::String maybe_unicode_message;

    results = callback.apply( args );
    retcode = results[0];
    maybe_unicode_message = results[1];
    Py::String message( maybe_unicode_message.encode( "utf-8" ) );

    // true returned
    if( long( retcode ) != 0 )
    {
        // copy out the answers
        msg = message.as_std_string();

        return true;
    }

    return false;
}
