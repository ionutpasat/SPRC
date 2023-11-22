/*
 * Please do not edit this file.
 * It was generated using rpcgen.
 */

#include "tema1.h"
#include <stdio.h>
#include <stdlib.h>
#include <rpc/pmap_clnt.h>
#include <string.h>
#include <memory.h>
#include <sys/socket.h>
#include <netinet/in.h>

#ifndef SIG_PF
#define SIG_PF void(*)(int)
#endif

// Create a vector to store the user IDs
vector<string> userIds;
// Create a vector to store the resources
vector<string> resourceNames;
// Create a list to store the data
vector<map<string, vector<string>>> approvals;

static void
tema1_prog_1(struct svc_req *rqstp, SVCXPRT *transp)
{
	union {
		char *request_authorization_1_arg;
		struct request_access_arg request_access_token_1_arg;
		struct validate_action_arg validate_delegated_action_1_arg;
		char *approve_request_token_1_arg;
	} argument;
	char *result;
	xdrproc_t _xdr_argument, _xdr_result;
	char *(*local)(char *, struct svc_req *);

	switch (rqstp->rq_proc) {
	case NULLPROC:
		(void) svc_sendreply (transp, (xdrproc_t) xdr_void, (char *)NULL);
		return;

	case request_authorization:
		_xdr_argument = (xdrproc_t) xdr_wrapstring;
		_xdr_result = (xdrproc_t) xdr_wrapstring;
		local = (char *(*)(char *, struct svc_req *)) request_authorization_1_svc;
		break;

	case request_access_token:
		_xdr_argument = (xdrproc_t) xdr_request_access_arg;
		_xdr_result = (xdrproc_t) xdr_request_access_response;
		local = (char *(*)(char *, struct svc_req *)) request_access_token_1_svc;
		break;

	case validate_delegated_action:
		_xdr_argument = (xdrproc_t) xdr_validate_action_arg;
		_xdr_result = (xdrproc_t) xdr_validate_action_response;
		local = (char *(*)(char *, struct svc_req *)) validate_delegated_action_1_svc;
		break;

	case approve_request_token:
		_xdr_argument = (xdrproc_t) xdr_wrapstring;
		_xdr_result = (xdrproc_t) xdr_approve_request_response;
		local = (char *(*)(char *, struct svc_req *)) approve_request_token_1_svc;
		break;

	default:
		svcerr_noproc (transp);
		return;
	}
	memset ((char *)&argument, 0, sizeof (argument));
	if (!svc_getargs (transp, (xdrproc_t) _xdr_argument, (caddr_t) &argument)) {
		svcerr_decode (transp);
		return;
	}
	result = (*local)((char *)&argument, rqstp);
	if (result != NULL && !svc_sendreply(transp, (xdrproc_t) _xdr_result, result)) {
		svcerr_systemerr (transp);
	}
	if (!svc_freeargs (transp, (xdrproc_t) _xdr_argument, (caddr_t) &argument)) {
		fprintf (stderr, "%s", "unable to free arguments");
		exit (1);
	}
	return;
}

int
main (int argc, char **argv)
{
	SVCXPRT *transp;

	pmap_unset (tema1_prog, tema1_vers);

	setbuf(stdout, NULL);

	transp = svcudp_create(RPC_ANYSOCK);
	if (transp == NULL) {
		fprintf (stderr, "%s", "cannot create udp service.");
		exit(1);
	}
	if (!svc_register(transp, tema1_prog, tema1_vers, tema1_prog_1, IPPROTO_UDP)) {
		fprintf (stderr, "%s", "unable to register (tema1_prog, tema1_vers, udp).");
		exit(1);
	}

	transp = svctcp_create(RPC_ANYSOCK, 0, 0);
	if (transp == NULL) {
		fprintf (stderr, "%s", "cannot create tcp service.");
		exit(1);
	}
	if (!svc_register(transp, tema1_prog, tema1_vers, tema1_prog_1, IPPROTO_TCP)) {
		fprintf (stderr, "%s", "unable to register (tema1_prog, tema1_vers, tcp).");
		exit(1);
	}

	ifstream ids_file(argv[1]);
	ifstream resources_file(argv[2]);
	ifstream approvals_file(argv[3]);
	int token_lifetime = atoi(argv[4]);

	if (!ids_file.is_open()) {
        cerr << "Error opening the ids_file." << endl;
        return 1;
    }

	if (!resources_file.is_open()) {
        cerr << "Error opening the file." << endl;
        return 1;
    }

    if (!approvals_file.is_open()) {
        cerr << "Error opening the approvals_file." << endl;
        return 1;
    }

	int numIds;
    ids_file >> numIds;

    // Read each user ID from the file
    string userId;
    for (int i = 0; i < numIds; ++i) {
        ids_file >> userId;
        userIds.push_back(userId);
    }

    // Close the file
    ids_file.close();

    // Print the stored user IDs
    // cout << "User IDs:" << endl;
    // for (const auto& id : userIds) {
    //     cout << id << endl;
    // }

	// Read the number of resources
    int numResources;
    resources_file >> numResources;

    // Read each resource name from the file
    string resourceName;
    for (int i = 0; i < numResources; ++i) {
        resources_file >> resourceName;
        resourceNames.push_back(resourceName);
    }

    // Close the file
    resources_file.close();

    // Print the stored resource names
    // cout << "Resource Names:" << endl;
    // for (const auto& resource : resourceNames) {
    //     cout << resource << endl;
    // }

    // Read each line from the file
    string line;
    while (getline(approvals_file, line)) {
        istringstream iss(line);

        // Parse the comma-separated values
        string token;
        map<string, vector<string>> fileEntry;

        while (getline(iss, token, ',')) {

            // Handle *,- case
            if (token == "*") {
                // Add empty map to represent no permissions
                fileEntry = {};
            } else {
                // File name
                string key = token;

                // Check if the file name is in the resourceNames vector
                if (find(resourceNames.begin(), resourceNames.end(), key) != resourceNames.end()) {
                    // File permissions
                    getline(iss, token, ',');

                    // Split the permissions into a vector
                    vector<string> permissions;
                    for (char c : token) {
                        permissions.push_back(string(1, c));
                    }

                    fileEntry[key] = permissions;

                    // Add the file entry to the list
                } else {
                    // Skip this entry as it's not in the resourceNames vector
                    getline(iss, token, ',');  // Consume permissions part
                }
            }
        }
        // Add the list of file data to the main data list
        approvals.push_back(fileEntry);
    }

    // Close the file
    approvals_file.close();

    // Print the stored data
    // for (const auto& fileEntry : approvals) {
    //         if (!fileEntry.empty()) {
    //             for (const auto& entry : fileEntry) {
    //                 cout << "File: " << entry.first << ", Permissions: ";
    //                 for (const auto& permission : entry.second) {
    //                     cout << permission << " ";
    //                 }
    //                 cout << endl;
    //             }
    //         } else {
    //             cout << "No permissions for anything" << endl;
    //         }
    //     cout << "----------" << endl;
    // }

	svc_run ();
	fprintf (stderr, "%s", "svc_run returned");
	exit (1);
	/* NOTREACHED */
}
