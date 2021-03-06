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
//  pysvn_client_cmd_diff.cpp
//
#if defined( _MSC_VER )
// disable warning C4786: symbol greater than 255 character,
// nessesary to ignore as <map> causes lots of warning
#pragma warning(disable: 4786)
#endif

#include "pysvn.hpp"
#include "pysvn_static_strings.hpp"

class pysvn_apr_file
{
public:
    pysvn_apr_file( SvnPool &pool )
    : m_pool( pool )
    , m_apr_file( NULL )
    , m_filename( NULL )
    {
    }

    ~pysvn_apr_file()
    {
        close();
        if( m_filename )
            svn_error_clear( svn_io_remove_file( m_filename, m_pool ) );
    }

    void open_unique_file( const std::string &tmp_dir )
    {
        svn_error_t *error = svn_io_open_unique_file
            (
            &m_apr_file,
            &m_filename,
            tmp_dir.c_str(),
            ".tmp",
            false,
            m_pool
            );
        if( error != NULL )
            throw SvnException( error );
    }

    
    void open_tmp_file()
    {
        apr_status_t status = apr_file_open( &m_apr_file, m_filename, APR_READ, APR_OS_DEFAULT, m_pool );
        if( status )
        {
            std::string msg( "opening file " ); msg += m_filename;
            throw SvnException( svn_error_create( status, NULL, msg.c_str() ) );
        }
    }

    void close()
    {
        // only close if we have an open file
        if( m_apr_file == NULL )
        {
            return;
        }
        apr_file_t *apr_file = m_apr_file;

        // prevent closing the file twice
        m_apr_file = NULL;

        apr_status_t status = apr_file_close( apr_file );
        if( status )
        {
            std::string msg( "closing file " ); msg += m_filename;
            throw SvnException( svn_error_create( status, NULL, msg.c_str() ) );
        }
    }

    apr_file_t *file()
    {
        return m_apr_file;
    }

private:
    SvnPool &m_pool;
    apr_file_t *m_apr_file;
    const char *m_filename;
};

Py::Object pysvn_client::cmd_diff( const Py::Tuple &a_args, const Py::Dict &a_kws )
{
    static argument_description args_desc[] =
    {
    { true,  name_tmp_path },
    { true,  name_url_or_path },
    { false, name_revision1 },
    { false, name_url_or_path2 },
    { false, name_revision2 },
    { false, name_recurse },
    { false, name_ignore_ancestry },
    { false, name_diff_deleted },
#if defined( PYSVN_HAS_CLIENT_DIFF2 )
    { false, name_ignore_content_type },
#endif
#if defined( PYSVN_HAS_CLIENT_DIFF3 )
    { false, name_header_encoding },
    { false, name_diff_options },
#endif
#if defined( PYSVN_HAS_CLIENT_DIFF4 )
    { false, name_depth },
#endif
    { false, NULL }
    };
    FunctionArguments args( "diff", args_desc, a_args, a_kws );
    args.check();

    std::string tmp_path( args.getUtf8String( name_tmp_path ) );
    std::string path1( args.getUtf8String( name_url_or_path ) );
    svn_opt_revision_t revision1 = args.getRevision( name_revision1, svn_opt_revision_base );
    std::string path2( args.getUtf8String( name_url_or_path2, path1 ) );
    svn_opt_revision_t revision2 = args.getRevision( name_revision2, svn_opt_revision_working );
#if defined( PYSVN_HAS_CLIENT_DIFF4 )
    svn_depth_t depth = args.getDepth( name_depth, name_recurse, svn_depth_infinity );
#else
    bool recurse = args.getBoolean( name_recurse, true );
#endif
    bool ignore_ancestry = args.getBoolean( name_ignore_ancestry, true );
    bool diff_deleted = args.getBoolean( name_diff_deleted, true );
#if defined( PYSVN_HAS_CLIENT_DIFF2 )
    bool ignore_content_type = args.getBoolean( name_ignore_content_type, false );
#endif

    SvnPool pool( m_context );

#if defined( PYSVN_HAS_CLIENT_DIFF3 )
    std::string header_encoding( args.getUtf8String( name_header_encoding, empty_string ) );
    const char *header_encoding_ptr = APR_LOCALE_CHARSET;
    if( !header_encoding.empty() )
        header_encoding_ptr = header_encoding.c_str();

    apr_array_header_t *options = NULL;
    if( args.hasArg( name_diff_options ) )
    {
        options = arrayOfStringsFromListOfStrings( args.getArg( name_diff_options ), pool );
    }
    else
    {
        options = apr_array_make( pool, 0, sizeof( const char * ) );
    }
#else
    apr_array_header_t *options = apr_array_make( pool, 0, sizeof( const char * ) );
#endif

    svn_stringbuf_t *stringbuf = NULL;

    try
    {
        std::string norm_tmp_path( svnNormalisedIfPath( tmp_path, pool ) );
        std::string norm_path1( svnNormalisedIfPath( path1, pool ) );
        std::string norm_path2( svnNormalisedIfPath( path2, pool ) );

        checkThreadPermission();

        pysvn_apr_file output_file( pool );
        pysvn_apr_file error_file( pool );

        output_file.open_unique_file( norm_tmp_path );
        error_file.open_unique_file( norm_tmp_path );

        PythonAllowThreads permission( m_context );

#if defined( PYSVN_HAS_CLIENT_DIFF4 )
        svn_error_t *error = svn_client_diff3
            (
            options,
            norm_path1.c_str(), &revision1,
            norm_path2.c_str(), &revision2,
            depth,
            ignore_ancestry,
            !diff_deleted,
            ignore_content_type,
            header_encoding_ptr,
            output_file.file(),
            error_file.file(),
            m_context,
            pool
            );
#elif defined( PYSVN_HAS_CLIENT_DIFF3 )
        svn_error_t *error = svn_client_diff3
            (
            options,
            norm_path1.c_str(), &revision1,
            norm_path2.c_str(), &revision2,
            recurse,
            ignore_ancestry,
            !diff_deleted,
            ignore_content_type,
            header_encoding_ptr,
            output_file.file(),
            error_file.file(),
            m_context,
            pool
            );
#elif defined( PYSVN_HAS_CLIENT_DIFF2 )
        svn_error_t *error = svn_client_diff2
            (
            options,
            norm_path1.c_str(), &revision1,
            norm_path2.c_str(), &revision2,
            recurse,
            ignore_ancestry,
            !diff_deleted,
            ignore_content_type,
            output_file.file(),
            error_file.file(),
            m_context,
            pool
            );
#else
        svn_error_t *error = svn_client_diff
            (
            options,
            norm_path1.c_str(), &revision1,
            norm_path2.c_str(), &revision2,
            recurse,
            ignore_ancestry,
            !diff_deleted,
            output_file.file(),
            error_file.file(),
            m_context,
            pool
            );
#endif
        permission.allowThisThread();
        if( error != NULL )
            throw SvnException( error );

        output_file.close();

        output_file.open_tmp_file();
        error = svn_stringbuf_from_aprfile( &stringbuf, output_file.file(), pool );
        if( error != NULL )
            throw SvnException( error );
    }
    catch( SvnException &e )
    {
        // use callback error over ClientException
        m_context.checkForError( m_module.client_error );

        throw_client_error( e );
    }

    // cannot convert to Unicode as we have no idea of the encoding of the bytes
    return Py::String( stringbuf->data, (int)stringbuf->len );
}

#if defined( PYSVN_HAS_CLIENT_DIFF_PEG )
Py::Object pysvn_client::cmd_diff_peg( const Py::Tuple &a_args, const Py::Dict &a_kws )
{
    static argument_description args_desc[] =
    {
    { true,  name_tmp_path },
    { true,  name_url_or_path },
    { false, name_peg_revision },
    { false, name_revision_start },
    { false, name_revision_end },
    { false, name_recurse },
    { false, name_ignore_ancestry },
    { false, name_diff_deleted },
#if defined( PYSVN_HAS_CLIENT_DIFF_PEG2 )
    { false, name_ignore_content_type },
#endif
#if defined( PYSVN_HAS_CLIENT_DIFF_PEG3 )
    { false, name_header_encoding },
    { false, name_diff_options },
#endif
#if defined( PYSVN_HAS_CLIENT_DIFF_PEG4 )
    { false, name_depth },
    { false, name_relative_to_dir },
    { false, name_changelists },
#endif
    { false, NULL }
    };
    FunctionArguments args( "diff_peg", args_desc, a_args, a_kws );
    args.check();

    std::string tmp_path( args.getUtf8String( name_tmp_path ) );
    std::string path( args.getUtf8String( name_url_or_path ) );
    svn_opt_revision_t revision_start = args.getRevision( name_revision_start, svn_opt_revision_base );
    svn_opt_revision_t revision_end = args.getRevision( name_revision_end, svn_opt_revision_working );
    svn_opt_revision_t peg_revision = args.getRevision( name_peg_revision, revision_end );

    SvnPool pool( m_context );

#if defined( PYSVN_HAS_CLIENT_DIFF_PEG4 )
    svn_depth_t depth = args.getDepth( name_depth, name_recurse, svn_depth_infinity );
    std::string std_relative_to_dir;
    const char *relative_to_dir = NULL;
    if( args.hasArg( name_relative_to_dir ) )
    {
        std_relative_to_dir = args.getString( name_relative_to_dir );
        relative_to_dir = std_relative_to_dir.c_str();
    }

    apr_array_header_t *changelists = NULL;

    if( args.hasArg( name_changelists ) )
    {
        changelists = arrayOfStringsFromListOfStrings( args.getArg( name_changelists ), pool );
    }
#else
    bool recurse = args.getBoolean( name_recurse, true );
#endif
    bool ignore_ancestry = args.getBoolean( name_ignore_ancestry, true );
    bool diff_deleted = args.getBoolean( name_diff_deleted, true );
#if defined( PYSVN_HAS_CLIENT_DIFF_PEG2 )
    bool ignore_content_type = args.getBoolean( name_ignore_content_type, false );
#endif

#if defined( PYSVN_HAS_CLIENT_DIFF_PEG3 )
    std::string header_encoding( args.getUtf8String( name_header_encoding, empty_string ) );
    const char *header_encoding_ptr = APR_LOCALE_CHARSET;
    if( !header_encoding.empty() )
        header_encoding_ptr = header_encoding.c_str();

    apr_array_header_t *options = NULL;
    if( args.hasArg( name_diff_options ) )
    {
        options = arrayOfStringsFromListOfStrings( args.getArg( name_diff_options ), pool );
    }
    else
    {
        options = apr_array_make( pool, 0, sizeof( const char * ) );
    }
#else
    apr_array_header_t *options = apr_array_make( pool, 0, sizeof( const char * ) );
#endif

    bool is_url = is_svn_url( path );
    revisionKindCompatibleCheck( is_url, peg_revision, name_peg_revision, name_url_or_path );
    revisionKindCompatibleCheck( is_url, revision_start, name_revision_start, name_url_or_path );
    revisionKindCompatibleCheck( is_url, revision_end, name_revision_end, name_url_or_path );

    svn_stringbuf_t *stringbuf = NULL;

    try
    {
        std::string norm_tmp_path( svnNormalisedIfPath( tmp_path, pool ) );
        std::string norm_path( svnNormalisedIfPath( path, pool ) );

        checkThreadPermission();

        PythonAllowThreads permission( m_context );
        pysvn_apr_file output_file( pool );
        pysvn_apr_file error_file( pool );

        output_file.open_unique_file( norm_tmp_path );
        error_file.open_unique_file( norm_tmp_path );

        // std::cout << "peg_revision "    << peg_revision.kind    << " " << peg_revision.value.number     << std::endl;
        // std::cout << "revision_start "  << revision_start.kind  << " " << revision_start.value.number   << std::endl;
        // std::cout << "revision_end "    << revision_end.kind    << " " << revision_end.value.number     << std::endl;

#if defined( PYSVN_HAS_CLIENT_DIFF_PEG4 )
        svn_error_t *error = svn_client_diff_peg4
            (
            options,
            norm_path.c_str(),
            &peg_revision,
            &revision_start,
            &revision_end,
            relative_to_dir,
            depth,
            ignore_ancestry,
            !diff_deleted,
            ignore_content_type,
            header_encoding_ptr,
            output_file.file(),
            error_file.file(),
            changelists,
            m_context,
            pool
            );
#elif defined( PYSVN_HAS_CLIENT_DIFF_PEG3 )
        svn_error_t *error = svn_client_diff_peg3
            (
            options,
            norm_path.c_str(),
            &peg_revision,
            &revision_start,
            &revision_end,
            recurse,
            ignore_ancestry,
            !diff_deleted,
            ignore_content_type,
            header_encoding_ptr,
            output_file.file(),
            error_file.file(),
            m_context,
            pool
            );
#elif defined( PYSVN_HAS_CLIENT_DIFF_PEG2 )
        svn_error_t *error = svn_client_diff_peg2
            (
            options,
            norm_path.c_str(),
            &peg_revision,
            &revision_start,
            &revision_end,
            recurse,
            ignore_ancestry,
            !diff_deleted,
            ignore_content_type,
            output_file.file(),
            error_file.file(),
            m_context,
            pool
            );
#else
        svn_error_t *error = svn_client_diff_peg
            (
            options,
            norm_path.c_str(),
            &peg_revision,
            &revision_start,
            &revision_end,
            recurse,
            ignore_ancestry,
            !diff_deleted,
            output_file.file(),
            error_file.file(),
            m_context,
            pool
            );
#endif
        permission.allowThisThread();
        if( error != NULL )
            throw SvnException( error );

        output_file.close();

        output_file.open_tmp_file();
        error = svn_stringbuf_from_aprfile( &stringbuf, output_file.file(), pool );
        if( error != NULL )
            throw SvnException( error );
    }
    catch( SvnException &e )
    {
        // use callback error over ClientException
        m_context.checkForError( m_module.client_error );

        throw_client_error( e );
    }

    // cannot convert to Unicode as we have no idea of the encoding of the bytes
    return Py::String( stringbuf->data, (int)stringbuf->len );
}
#endif

#if defined( PYSVN_HAS_CLIENT_DIFF_SUMMARIZE )
class DiffSummarizeBaton
{
public:
    DiffSummarizeBaton( PythonAllowThreads *permission, Py::List &diff_list )
        : m_permission( permission )
        , m_diff_list( diff_list )
        {}
    ~DiffSummarizeBaton()
        {}

    PythonAllowThreads  *m_permission;

    DictWrapper         *m_wrapper_diff_summary;
    Py::List            &m_diff_list;
};

extern "C"
{
svn_error_t *diff_summarize_c
    (
    const svn_client_diff_summarize_t *diff,
    void *baton_,
    apr_pool_t *pool
    )
{
    DiffSummarizeBaton *baton = reinterpret_cast<DiffSummarizeBaton *>( baton_ );

    PythonDisallowThreads callback_permission( baton->m_permission );

    Py::Dict diff_dict;

    diff_dict[ *py_name_path ] = Py::String( diff->path, name_utf8 );
    diff_dict[ *py_name_summarize_kind ] = toEnumValue( diff->summarize_kind );
    diff_dict[ *py_name_prop_changed ] = Py::Int( diff->prop_changed != 0 );
    diff_dict[ *py_name_node_kind ] = toEnumValue( diff->node_kind );

    baton->m_diff_list.append( baton->m_wrapper_diff_summary->wrapDict( diff_dict ) );

    return SVN_NO_ERROR;
}
}

Py::Object pysvn_client::cmd_diff_summarize( const Py::Tuple &a_args, const Py::Dict &a_kws )
{
    static argument_description args_desc[] =
    {
    { true,  name_url_or_path1 },
    { false, name_revision1 },
    { false, name_url_or_path2 },
    { false, name_revision2 },
    { false, name_recurse },
    { false, name_ignore_ancestry },
#if defined( PYSVN_HAS_CLIENT_DIFF_SUMMARIZE2 )
    { false, name_depth },
    { false, name_changelists },
#endif
    { false, NULL }
    };
    FunctionArguments args( "diff_summarize", args_desc, a_args, a_kws );
    args.check();

    std::string path1( args.getUtf8String( name_url_or_path1 ) );
    svn_opt_revision_t revision1 = args.getRevision( name_revision1, svn_opt_revision_base );
    std::string path2( args.getUtf8String( name_url_or_path2, path1 ) );
    svn_opt_revision_t revision2 = args.getRevision( name_revision2, svn_opt_revision_working );

    SvnPool pool( m_context );

#if defined( PYSVN_HAS_CLIENT_DIFF_SUMMARIZE2 )
    svn_depth_t depth = args.getDepth( name_depth, name_recurse, svn_depth_infinity );

    apr_array_header_t *changelists = NULL;

    if( args.hasArg( name_changelists ) )
    {
        changelists = arrayOfStringsFromListOfStrings( args.getArg( name_changelists ), pool );
    }
#else
    bool recurse = args.getBoolean( name_recurse, true );
#endif
    bool ignore_ancestry = args.getBoolean( name_ignore_ancestry, true );

    Py::List diff_list;

    try
    {
        std::string norm_path1( svnNormalisedIfPath( path1, pool ) );
        std::string norm_path2( svnNormalisedIfPath( path2, pool ) );

        checkThreadPermission();

        PythonAllowThreads permission( m_context );

        DiffSummarizeBaton diff_baton( &permission, diff_list );
        diff_baton.m_wrapper_diff_summary = &m_wrapper_diff_summary;

#if defined( PYSVN_HAS_CLIENT_DIFF_SUMMARIZE2 )
        svn_error_t *error = svn_client_diff_summarize2
            (
            norm_path1.c_str(),
            &revision1,
            norm_path2.c_str(),
            &revision2,
            depth,
            ignore_ancestry,
            changelists,
            diff_summarize_c,
            reinterpret_cast<void *>( &diff_baton ),
            m_context,
            pool
            );
#else
        svn_error_t *error = svn_client_diff_summarize
            (
            norm_path1.c_str(),
            &revision1,
            norm_path2.c_str(),
            &revision2,
            recurse,
            ignore_ancestry,
            diff_summarize_c,
            reinterpret_cast<void *>( &diff_baton ),
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

    // cannot convert to Unicode as we have no idea of the encoding of the bytes
    return diff_list;
}

Py::Object pysvn_client::cmd_diff_summarize_peg( const Py::Tuple &a_args, const Py::Dict &a_kws )
{
    static argument_description args_desc[] =
    {
    { true,  name_url_or_path },
    { false, name_peg_revision },
    { false, name_revision_start },
    { false, name_revision_end },
    { false, name_recurse },
    { false, name_ignore_ancestry },
#if defined( PYSVN_HAS_CLIENT_DIFF_SUMMARIZE_PEG2 )
    { false, name_depth },
    { false, name_changelists },
#endif
    { false, NULL }
    };
    FunctionArguments args( "diff_summarize_peg", args_desc, a_args, a_kws );
    args.check();

    std::string path( args.getUtf8String( name_url_or_path ) );
    svn_opt_revision_t revision_start = args.getRevision( name_revision_start, svn_opt_revision_base );
    svn_opt_revision_t revision_end = args.getRevision( name_revision_end, svn_opt_revision_working );
    svn_opt_revision_t peg_revision = args.getRevision( name_peg_revision, revision_end );

    SvnPool pool( m_context );

#if defined( PYSVN_HAS_CLIENT_DIFF_SUMMARIZE_PEG2 )
    svn_depth_t depth = args.getDepth( name_depth, name_recurse, svn_depth_infinity );
    apr_array_header_t *changelists = NULL;

    if( args.hasArg( name_changelists ) )
    {
        changelists = arrayOfStringsFromListOfStrings( args.getArg( name_changelists ), pool );
    }
#else
    bool recurse = args.getBoolean( name_recurse, true );
#endif
    bool ignore_ancestry = args.getBoolean( name_ignore_ancestry, true );

    bool is_url = is_svn_url( path );
    revisionKindCompatibleCheck( is_url, peg_revision, name_peg_revision, name_url_or_path );
    revisionKindCompatibleCheck( is_url, revision_start, name_revision_start, name_url_or_path );
    revisionKindCompatibleCheck( is_url, revision_end, name_revision_end, name_url_or_path );

    Py::List diff_list;

    try
    {
        std::string norm_path( svnNormalisedIfPath( path, pool ) );

        checkThreadPermission();

        PythonAllowThreads permission( m_context );

        DiffSummarizeBaton diff_baton( &permission, diff_list );
        diff_baton.m_wrapper_diff_summary = &m_wrapper_diff_summary;

#if defined( PYSVN_HAS_CLIENT_DIFF_SUMMARIZE_PEG2 )
        svn_error_t *error = svn_client_diff_summarize_peg2
            (
            norm_path.c_str(),
            &peg_revision,
            &revision_start,
            &revision_end,
            depth,
            ignore_ancestry,
            changelists,
            diff_summarize_c,
            reinterpret_cast<void *>( &diff_baton ),
            m_context,
            pool
            );
#else
        svn_error_t *error = svn_client_diff_summarize_peg
            (
            norm_path.c_str(),
            &peg_revision,
            &revision_start,
            &revision_end,
            recurse,
            ignore_ancestry,
            diff_summarize_c,
            reinterpret_cast<void *>( &diff_baton ),
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

    // cannot convert to Unicode as we have no idea of the encoding of the bytes
    return diff_list;
}
#endif
