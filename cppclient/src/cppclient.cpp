//============================================================================
// Name        : cppclient.cpp
// Author      : Andreas Hermann
// Version     : 0.1
// Copyright   : 
// Description : Hello World, from C++ to Neo4J and back
//============================================================================

#include <iostream>
using namespace std;

#include "zmqpp/zmqpp.hpp"
#include "stdio.h"
#include "string.h"
#include "json/json.h"


int main()
{

  auto context = zmq_init(1);
  auto zsock = zmq_socket(context, ZMQ_REQ);
  zmq_connect(zsock, "tcp://localhost:5555");

  Json::FastWriter js_writer;
  Json::Value js_msg(Json::objectValue);
  Json::Value js_data(Json::objectValue);
  Json::Value js_params(Json::objectValue);
  Json::Value js_path(Json::objectValue);

  js_data["city"] = "Dallas";
  js_data["name"] = "Frank";

  Json::Value js_array(Json::arrayValue);

  js_msg["data"] = js_data;
  js_msg["params"] = js_params;
  js_msg["path"] = Json::Value("wordgraph/vertices/create");


  string msg_to_send;
  msg_to_send = js_writer.write(js_msg);

  std::cout << "Trying to send " << msg_to_send << std::endl;
  zmq_send(zsock, msg_to_send.c_str(), msg_to_send.length(), 0);

  zmq_msg_t message;
  zmq_msg_init(&message);

    zmq_recvmsg(zsock, &message, 0);
    std::string str_message(static_cast<char*> (zmq_msg_data(&message)), zmq_msg_size(&message));

  zmq_close(zsock);
  zmq_term( context);

  Json::Reader js_reader;
  Json::Value js_rcv;
  if(js_reader.parse(str_message, js_rcv, false))
  {
    cout << "Received: " << js_rcv << endl; // prints !!!Hello World!!!
  }else{
    cout << "Error parsing the answer from server" << std::endl;
  }
  return 0;
}
