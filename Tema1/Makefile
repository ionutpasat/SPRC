
# This is a template Makefile generated by rpcgen

# Parameters

CLIENT = tema1_client
SERVER = tema1_server

SOURCES_CLNT.cpp = 
SOURCES_CLNT.h = 
SOURCES_SVC.cpp = 
SOURCES_SVC.h = 
SOURCES.x = tema1.x

TARGETS_SVC.cpp = tema1_svc.cpp tema1_server.cpp tema1_xdr.cpp 
TARGETS_CLNT.cpp = tema1_clnt.cpp tema1_client.cpp tema1_xdr.cpp 
TARGETS = tema1.h tema1_xdr.cpp tema1_clnt.cpp tema1_svc.cpp tema1_client.cpp tema1_server.cpp

OBJECTS_CLNT = $(SOURCES_CLNT.cpp:%.cpp=%.o) $(TARGETS_CLNT.cpp:%.cpp=%.o)
OBJECTS_SVC = $(SOURCES_SVC.cpp:%.cpp=%.o) $(TARGETS_SVC.cpp:%.cpp=%.o)
# Compiler flags 

CPPFLAGS += -g -I/usr/include/tirpc 
LDLIBS += -lnsl -ltirpc
RPCGENFLAGS = 

# Targets 

all : $(CLIENT) $(SERVER)

$(TARGETS) : $(SOURCES.x) 
	rpcgen $(RPCGENFLAGS) $(SOURCES.x)

$(OBJECTS_CLNT) : $(SOURCES_CLNT.cpp) $(SOURCES_CLNT.h) $(TARGETS_CLNT.cpp) 

$(OBJECTS_SVC) : $(SOURCES_SVC.cpp) $(SOURCES_SVC.h) $(TARGETS_SVC.cpp) 

$(CLIENT) : $(OBJECTS_CLNT) 
	$(LINK.cpp) -o $(CLIENT) $(OBJECTS_CLNT) $(LDLIBS) 

$(SERVER) : $(OBJECTS_SVC) 
	$(LINK.cpp) -o $(SERVER) $(OBJECTS_SVC) $(LDLIBS) 

 clean:
	 $(RM) $(OBJECTS_CLNT) $(OBJECTS_SVC) $(CLIENT) $(SERVER)

