struct request_access_arg {
	string name<>;
	string request_token<>;
	int with_refresh;
};

struct request_access_response {
	string access_token<>;
	string refresh_token<>;
	string error_message<>;
	int error_flag;
};

struct validate_action_arg {
	string operation<>;
	string resource<>;
	string access_token<>;
};

struct validate_action_response {
	string result<>;
	string new_access_token<>;
	int access_token_refreshed;
};

struct approve_request_response {
	string request_token<>;
	int with_sign;
};

program tema1_prog {
	version tema1_vers {
		string request_authorization(string) = 1;
		struct request_access_response request_access_token(struct request_access_arg) = 2;
		struct validate_action_response validate_delegated_action(struct validate_action_arg) = 3;
		struct approve_request_response approve_request_token(string) = 4;
	} = 1;
} = 123456789;