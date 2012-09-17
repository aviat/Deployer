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
//  pysvn_client_cmd_prop.cpp
//
#if defined( _MSC_VER )
// disable warning C4786: symbol greater than 255 character,
// nessesary to ignore as <map> causes lots of warning
#pragma warning(disable: 4786)
#endif

#include "pysvn.hpp"
#include "pysvn_static_strings.hpp"

Py::Object pysvn_client::cmd_relocate( const Py::Tuple &a_args, const Py::Dict &a_kws )
{
    static argument_description args_desc[] =
    {
    { true,  name_from_url },
    { true,  name_to_url },
    { true,  name_path },
    { false, name_recurse },
    { false, NULL }
    };
    FunctionArguments args( "relocate", args_desc, a_args, a_kws );
    args.check();

    std::string from_url( args.getUtf8String( name_from_url ) );
    std::string to_url( args.getUtf8String( name_to_url ) );
    std::string path( args.getUtf8String( name_path ) );

    bool recurse = args.getBoolean( name_recurse, true );

    SvnPool pool( m_context );

    try
    {
        std::string norm_path( svnNormalisedIfPath( path, pool ) );

        checkThreadPermission();

        PythonAllowThreads permission( m_context );
        svn_error_t * error = svn_client_relocate
            (
            norm_path.c_str(),
            from_url.c_str(),
            to_url.c_str(),
            recurse,
            m_context,
            pool
            );
        permission.allowThisThread();
        if( error != NULL )
            throw SvnException( error );
    }
    catch( SvnException &e )
    {
        // use callback error over ClientException
        m_context.checkForError( m_module.client_error );

        throw_client_error( e );
    }

    return Py::None();
}

Py::Object pysvn_client::cmd_switch( const Py::Tuple &a_args, const Py::Dict &a_kws )
{
    static argument_description args_desc[] =
    {
    { true,  name_path },
    { true,  name_url },
    { false, name_recurse },
    { false, name_revision },
#if defined( PYSVN_HAS_CLIENT_SWITCH2 )
    { false, name_depth },
#endif
    { false, NULL }
    };
    FunctionArguments args( "switch", args_desc, a_args, a_kws );
    args.check();

    std::string path( args.getUtf8String( name_path ) );
    std::string url( args.getUtf8String( name_url ) );
    svn_opt_revision_t revision = args.getRevision( name_revision, svn_opt_revision_head );
#if defined( PYSVN_HAS_CLIENT_SWITCH2 )
    svn_depth_t depth = args.getDepth( name_depth, name_recurse, svn_depth_infinity );
#else
    bool recurse = args.getBoolean( name_recurse, true );
#endif
    SvnPool pool( m_context );

    svn_revnum_t revnum = 0;
    try
    {
        std::string norm_path( svnNormalisedIfPath( path, pool ) );

        checkThreadPermission();

        PythonAllowThreads permission( m_context );

#if defined( PYSVN_HAS_CLIENT_SWITCH2 )
        svn_error_t *error = svn_client_switch
            (
            &revnum,
            norm_path.c_str(),
            url.c_str(),
            &revision,
            depth,
            m_context,
            pool
            );
#else
        svn_error_t *error = svn_client_switch
            (
            &revnum,
            norm_path.c_str(),
            url.c_str(),
            &revision,
            recurse,
            m_context,
            pool
            );
#endif
        permission.allowThisThread();
        if( error != NULL )
            throw SvnException( error );
    }
    catch( SvnException &e )
    {
        // use callback error over ClientException
        m_context.checkForError( m_module.client_error );

        throw_client_error( e );
    }

    return Py::asObject( new pysvn_revision( svn_opt_revision_number, 0, revnum ) );
}
