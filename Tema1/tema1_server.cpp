/*
 * This is sample code generated by rpcgen.
 * These are only templates and you can use them
 * as a guideline for developing your own functions.
 */

#include "tema1.h"
#include "token.h"

unordered_map<string, vector<string>> users; 
int approval_index = 0;

char **
request_authorization_1_svc(char **argp, struct svc_req *rqstp)
{
	static char * result;
	string userId = string(*argp);
	cout << "BEGIN " << userId << " AUTHZ" << endl;
	if (find(userIds.begin(), userIds.end(), userId) != userIds.end()) {
		result = generate_access_token(*argp);
		string req_token = string(*(&result));
		users[userId].push_back(req_token);
	}
	else {
		result = (char *) USER_NOT_FOUND;
		return &result;
	}


	return &result;
}

struct request_access_response *
request_access_token_1_svc(struct request_access_arg *argp, struct svc_req *rqstp)
{
	static struct request_access_response result;
	result.access_token = generate_access_token(argp->request_token);
	users[string(argp->name)].push_back(string(*(&result.access_token)));
	cout << "  AccessToken = " << *(&result.access_token) << endl;
	if (argp->with_refresh == 1) {
		result.refresh_token = generate_access_token(*(&result.access_token));
		users[string(argp->name)].push_back(string(*(&result.refresh_token)));
	}
	else {
		result.refresh_token = (char *) NO_REFRESH_TOKEN;
	}
	result.error_flag = 0;
	result.error_message = (char *) NO_ERROR;
	approval_index++;
	// string userId = string(argp->name);
	// string req_token = string(argp->request_token);
	// int refresh = argp->with_refresh;
	// users[userId].push_back(to_string(approval_index));
	// approval_index++;
	// result.access_token = generate_access_token((char *)req_token.c_str());
	// if (refresh == 1) {
	// 	result.refresh_token = generate_access_token(*(&result.access_token));
	// }
	// else {
	// 	result.refresh_token = (char *) NO_REFRESH_TOKEN;
	// }

	return &result;
}

struct validate_action_response *
validate_delegated_action_1_svc(struct validate_action_arg *argp, struct svc_req *rqstp)
{
	static struct validate_action_response  result;

	string operation = string(argp->operation);
	string resource = string(argp->resource);
	string access_token = string(argp->access_token);

	int n = 0;
	for (auto& user : users) {
		if (user.second.size() > 1 && user.second[1] == access_token) {
			if (operation == READ) {
				if (find(approvals.at(n)[resource].begin(), approvals.at(n)[resource].end(), "R") != approvals.at(n)[resource].end()) {
					result.result = (char *) PERMISSION_GRANTED;
				}
				else {
					result.result = (char *) PERMISSION_DENIED;
				}
			}
			if (operation == INSERT) {
				if (find(approvals.at(n)[resource].begin(), approvals.at(n)[resource].end(), "I") != approvals.at(n)[resource].end()) {
					result.result = (char *) PERMISSION_GRANTED;
				}
				else {
					result.result = (char *) PERMISSION_DENIED;
				}
			}
			if (operation == MODIFY) {
				if (find(approvals.at(n)[resource].begin(), approvals.at(n)[resource].end(), "M") != approvals.at(n)[resource].end()) {
					result.result = (char *) PERMISSION_GRANTED;
				}
				else {
					result.result = (char *) PERMISSION_DENIED;
				}
			}
			if (operation == DELETE) {
				if (find(approvals.at(n)[resource].begin(), approvals.at(n)[resource].end(), "D") != approvals.at(n)[resource].end()) {
					result.result = (char *) PERMISSION_GRANTED;
				}
				else {
					result.result = (char *) PERMISSION_DENIED;
				}
			}
			if (operation == EXECUTE) {
				if (find(approvals.at(n)[resource].begin(), approvals.at(n)[resource].end(), "X") != approvals.at(n)[resource].end()) {
					result.result = (char *) PERMISSION_GRANTED;
				}
				else {
					result.result = (char *) PERMISSION_DENIED;
				}
			}

		}
		n++;
	}

	return &result;
}

struct approve_request_response *
approve_request_token_1_svc(char **argp, struct svc_req *rqstp)
{
	static struct approve_request_response  result;
	if (!approvals.at(approval_index).empty()) {
		result.with_sign = 1;
		cout << "  RequestToken = " << *argp << endl;
	} else {
		result.with_sign = 0;
		cout << "  RequestToken = " << *argp << endl;
		approval_index++;
	}
	result.request_token = *argp;

	return &result;
}
