/*
 * This is sample code generated by rpcgen.
 * These are only templates and you can use them
 * as a guideline for developing your own functions.
 */

#include "tema1.h"

// Create a list to store the requests
list<pair<string, pair<string, string>>> requests;
// Create a map to store the users and their tokens
unordered_map<string, vector<string>> users;


void
tema1_prog_1(char *host)
{
	CLIENT *clnt;
	char * request_authorization_1_arg;
	char * *result_1;
	char * approve_request_token_1_arg;
	struct approve_request_response  *result_4;
	struct request_access_arg  request_access_token_1_arg;
	struct request_access_response  *result_2;
	struct validate_action_arg  validate_delegated_action_1_arg;
	struct validate_action_response  *result_3;

#ifndef	DEBUG
	clnt = clnt_create (host, tema1_prog, tema1_vers, "udp");
	if (clnt == NULL) {
		clnt_pcreateerror (host);
		exit (1);
	}
#endif	/* DEBUG */

	// Execute every request that was read
	for (const auto& request : requests) {
		// If it's a request for authorization
        if (request.second.first == REQUEST) {
			request_authorization_1_arg = (char *)request.first.c_str();
			// Call the first authorization process and get the request token
			result_1 = request_authorization_1(&request_authorization_1_arg, clnt);
			if (result_1 == (char **) NULL) {
				clnt_perror (clnt, "call failed");
			}
			string response = string(*result_1);
			// If the user was not found, print the error message
			if (response == USER_NOT_FOUND) {
				cout << USER_NOT_FOUND << endl;
				continue;
			} else {
				// If the user was found, store the request token
				if (users.find(request.first) == users.end()) {
				users[request.first].push_back(response);
				} else {
					users[request.first] = vector<string>();
					users[request.first].push_back(response);
				}
				// Call the second authorization process and get the request token signature
				approve_request_token_1_arg = (char *)response.c_str();
				result_4 = approve_request_token_1(&approve_request_token_1_arg, clnt);
				if (result_4 == (struct approve_request_response *) NULL) {
					clnt_perror (clnt, "call failed");
				}
				// If the request token signature is invalid, print the error message
				if (result_4->with_sign == 0) {
					cout << REQUEST_DENIED << endl;
					continue;
				} else {
					cout << response << " -> ";
				}
				// Call the third authorization process and get the access token
				// and the refresh token if the user requested it
				request_access_token_1_arg.name = (char *)request.first.c_str();
				request_access_token_1_arg.request_token = (char *)response.c_str();
				request_access_token_1_arg.with_refresh = stoi(request.second.second);
				result_2 = request_access_token_1(&request_access_token_1_arg, clnt);
				if (result_2 == (struct request_access_response *) NULL) {
					clnt_perror (clnt, "call failed");
				}
				users[request.first].push_back(string(result_2->access_token));
				cout << result_2->access_token;
				if (string(result_2->refresh_token) == (char *)NO_REFRESH_TOKEN) {
					cout << endl;
				} else {
					cout << "," << result_2->refresh_token << endl;
				}
			}

		} else {
			// If it's a request for executing a certain operation
			if (users.find(request.first) == users.end() || users[request.first].size() == 1) {
				validate_delegated_action_1_arg.access_token = (char *)NO_ACCESS_TOKEN;
			} else {
				string acc_token = users[request.first].at(1);
				char * accToken = (char *)acc_token.c_str();
				validate_delegated_action_1_arg.access_token = accToken;
			}
			// Make a call to the server to execute the operation
			validate_delegated_action_1_arg.operation = (char *)request.second.first.c_str();
			validate_delegated_action_1_arg.resource = (char *)request.second.second.c_str();
			result_3 = validate_delegated_action_1(&validate_delegated_action_1_arg, clnt);
			if (result_3 == (struct validate_action_response *) NULL) {
				clnt_perror (clnt, "call failed");
			}
			// If the access token expired, the server updated it and the client has to do so too
			if (result_3->access_token_refreshed == 1) {
				users[request.first].at(1) = string(result_3->new_access_token);
			}
			// Print the result of the operation
			cout << result_3->result << endl;
		}
    }

#ifndef	DEBUG
	clnt_destroy (clnt);
#endif	 /* DEBUG */
}


int main (int argc, char *argv[])
{
	char *host;

	if (argc < 2) {
		printf ("usage: %s server_host\n", argv[0]);
		exit (1);
	}
	host = argv[1];

	ifstream inputFile(argv[2]);
    if (!inputFile.is_open()) {
        cerr << "Unable to open the file." << endl;
        return 1;
    }

    // Read each line from the file
    string line;
    while (getline(inputFile, line)) {
        istringstream iss(line);

        // Parse the comma-separated values
        string client_id, operation_str, third_str;
        getline(iss, client_id, ',');
        getline(iss, operation_str, ',');
        getline(iss, third_str, ',');
		// Add the requests as a pair to the list
		requests.push_back({client_id, {operation_str, third_str}});

    }

    // Close the file
    inputFile.close();

	tema1_prog_1 (host);
    return 0;
}
