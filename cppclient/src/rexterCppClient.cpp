//============================================================================
// Name        : cppclient.cpp
// Author      : Andreas Hermann
// Version     : 0.1
// Copyright   : 
// Description : Hello Neo4J. From C++ to Neo4J and back
//============================================================================

// Bugs: send and receive always returns a EAGAIN error
// Todo: fix EAGAIN error

#include "rexterCppClient.h"

rexterCppClient::rexterCppClient(std::string zsock_addr)
  : connected(false)
{
  connect(zsock_addr);
}

rexterCppClient::~rexterCppClient()
{
  if(connected)
  {
    disconnect();
  }
}

int rexterCppClient::connect(std::string zsock_addr)
{
  zcontext = zmq_init(1);
  if (!zcontext) {
    std::cout << "Error occurred during zmq_init(): " << zmq_strerror(zmq_errno()) << std::endl;
    return -1;
  }
  zsock = zmq_socket(zcontext, ZMQ_REQ);
  if (!zsock) {
    std::cout << "Error occurred during zmq_socket(): " << zmq_strerror(zmq_errno()) << std::endl;
    return -1;
  }
  if(zmq_connect(zsock, zsock_addr.c_str()) != 0)
  {
    std::cout << "Error occurred during zmq_connect(): " << zmq_strerror(zmq_errno()) << std::endl;
    return -1;
  }
  connected = true;
  return 0;
}

int rexterCppClient::disconnect()
{
  if(connected)
  {
    std::cout << "Disconnecting from zsock" << std::endl;
    zmq_close(zsock);
    zmq_term(zcontext);
    connected = false;
  }
  return 0;
}

int rexterCppClient::send_request(const Json::Value &path, const Json::Value &params, const Json::Value &data, Json::Value &answer)
{

  // Code for sending:
  Json::Value js_msg(Json::objectValue);
  js_msg["data"] = data;
  js_msg["params"] = params;
  js_msg["path"] = path;
  std::string msg_to_send;
  msg_to_send = js_writer.write(js_msg);

  std::cout << "Trying to send " << msg_to_send << std::endl;

  if(zmq_send(zsock, msg_to_send.c_str(), msg_to_send.length(), 0) != 0)
  {
    std::cout << "Error sending message to server: " << zmq_errno() << " "
        << zmq_strerror(zmq_errno()) << std::endl;
    //return -1;
  }

  // Code for receiving:
  zmq_msg_t message;
  zmq_msg_init(&message);
  if(zmq_recvmsg(zsock, &message, 0) != 0)
  {
    std::cout << "Error receiving the answer from server: "
        << zmq_strerror(zmq_errno()) << std::endl;
    //return -1;
  }
  std::string str_message(static_cast<char*> (zmq_msg_data(&message)), zmq_msg_size(&message));
  zmq_msg_close (&message);

  // JSon parsing:
  Json::Value js_rcv;
  if(js_reader.parse(str_message, js_rcv, false))
  {
    std::cout << "Received: " << js_rcv << std::endl; // prints !!!Hello World!!!
    return 0;
  }else{
    std::cout << "Error parsing the answer from server" << std::endl;
    return -1;
  }
}

