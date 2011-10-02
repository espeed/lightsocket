//============================================================================
// Name        : cppclient.cpp
// Author      : Andreas Hermann
// Version     :
// Copyright   : 
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
using namespace std;

#include "zmqpp/zmqpp.hpp"
#include "stdio.h"
#include "string.h"


int main()
{

  auto context = zmq_init(1);
  auto zsock = zmq_socket(context, ZMQ_REQ);
  zmq_connect(zsock, "tcp://localhost:5555");

  //auto puller = zmq_socket(context, ZMQ_REQ);
  //zmq_bind(puller, "tcp://*:5555");

  string msg_to_send ("{\"data\": {\"city\": \"Dallas\", \"name\": \"James\"}, \"params\": \"\", \"path\": \"wordgraph/vertices/create\"}\n");
  //string msg_to_send ("Hwllo World!");
  std::cout << "Trying to send " << msg_to_send << std::endl;
  zmq_send(zsock, msg_to_send.c_str(), msg_to_send.length(), 0);

  zmq_msg_t message;
  zmq_msg_init(&message);

    zmq_recvmsg(zsock, &message, 0);
    std::string str_message(static_cast<char*> (zmq_msg_data(&message)), zmq_msg_size(&message));

  //zmq_close( pusher);
  zmq_close(zsock);

  zmq_term( context);

  cout << "Received: " << str_message << endl; // prints !!!Hello World!!!
  return 0;
}
