/*
 * Please do not edit this file.
 * It was generated using rpcgen.
 */

#ifndef _TEMA1_H_RPCGEN
#define _TEMA1_H_RPCGEN

#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <map>
#include <bits/stdc++.h>
#include <fstream>
#include <sstream>
#include <rpc/rpc.h>

using namespace std;

#define TOKEN_SIZE 16
#define LINE_SIZE 120

#define READ_ONLY "r"
#define TOKEN_DELIMS ",\r\n"

#define REQUEST "REQUEST"
#define USER_NOT_FOUND "USER_NOT_FOUND"
#define NO_REFRESH_TOKEN "NO_REFRESH_TOKEN"
#define NO_ACCESS_TOKEN "NO_ACCESS_TOKEN"
#define NO_ERROR "NO_ERROR"
#define ERROR_VALUE "ERROR_VALUE"
#define REQUEST_DENIED "REQUEST_DENIED"
#define PERMISSION_DENIED "PERMISSION_DENIED"
#define PERMISSION_GRANTED "PERMISSION_GRANTED"
#define TOKEN_EXPIRED "TOKEN_EXPIRED"
#define RESOURCE_NOT_FOUND "RESOURCE_NOT_FOUND"
#define OPERATION_NOT_PERMITTED "OPERATION_NOT_PERMITTED"
#define READ "READ"
#define INSERT "INSERT"
#define MODIFY "MODIFY"
#define DELETE "DELETE"
#define EXECUTE "EXECUTE"

 // Create a vector to store the user IDs
extern vector<string> userIds;
 // Create a vector to store the resources
extern vector<string> resourceNames;
// Create a vector to store the approvals for each request
extern vector<map<string, vector<string>>> approvals;
extern int token_lifetime;
int index = 0;

#ifdef __cplusplus
extern "C"
{
#endif

	struct request_access_arg
	{
		char *name;
		char *request_token;
		int with_refresh;
	};
	typedef struct request_access_arg request_access_arg;

	struct request_access_response
	{
		char *access_token;
		char *refresh_token;
		char *error_message;
		int error_flag;
	};
	typedef struct request_access_response request_access_response;

	struct validate_action_arg
	{
		char *operation;
		char *resource;
		char *access_token;
	};
	typedef struct validate_action_arg validate_action_arg;

	struct validate_action_response
	{
		char *result;
		char *new_access_token;
		int access_token_refreshed;
	};
	typedef struct validate_action_response validate_action_response;

	struct approve_request_response
	{
		char *request_token;
		int with_sign;
	};
	typedef struct approve_request_response approve_request_response;

#define tema1_prog 123456789
#define tema1_vers 1

#if defined(__STDC__) || defined(__cplusplus)
#define request_authorization 1
	extern char **request_authorization_1(char **, CLIENT *);
	extern char **request_authorization_1_svc(char **, struct svc_req *);
#define request_access_token 2
	extern struct request_access_response *request_access_token_1(struct request_access_arg *, CLIENT *);
	extern struct request_access_response *request_access_token_1_svc(struct request_access_arg *, struct svc_req *);
#define validate_delegated_action 3
	extern struct validate_action_response *validate_delegated_action_1(struct validate_action_arg *, CLIENT *);
	extern struct validate_action_response *validate_delegated_action_1_svc(struct validate_action_arg *, struct svc_req *);
#define approve_request_token 4
	extern struct approve_request_response *approve_request_token_1(char **, CLIENT *);
	extern struct approve_request_response *approve_request_token_1_svc(char **, struct svc_req *);
	extern int tema1_prog_1_freeresult(SVCXPRT *, xdrproc_t, caddr_t);

#else /* K&R C */
#define request_authorization 1
extern char **request_authorization_1();
extern char **request_authorization_1_svc();
#define request_access_token 2
extern struct request_access_response *request_access_token_1();
extern struct request_access_response *request_access_token_1_svc();
#define validate_delegated_action 3
extern struct validate_action_response *validate_delegated_action_1();
extern struct validate_action_response *validate_delegated_action_1_svc();
#define approve_request_token 4
extern struct approve_request_response *approve_request_token_1();
extern struct approve_request_response *approve_request_token_1_svc();
extern int tema1_prog_1_freeresult();
#endif /* K&R C */

	/* the xdr functions */

#if defined(__STDC__) || defined(__cplusplus)
	extern bool_t xdr_request_access_arg(XDR *, request_access_arg *);
	extern bool_t xdr_request_access_response(XDR *, request_access_response *);
	extern bool_t xdr_validate_action_arg(XDR *, validate_action_arg *);
	extern bool_t xdr_validate_action_response(XDR *, validate_action_response *);
	extern bool_t xdr_approve_request_response(XDR *, approve_request_response *);

#else /* K&R C */
extern bool_t xdr_request_access_arg();
extern bool_t xdr_request_access_response();
extern bool_t xdr_validate_action_arg();
extern bool_t xdr_validate_action_response();
extern bool_t xdr_approve_request_response();

#endif /* K&R C */

#ifdef __cplusplus
}
#endif

#endif /* !_TEMA1_H_RPCGEN */
