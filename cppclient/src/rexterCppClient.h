/*
 * cppclient.h
 *
 *  Created on: 04.10.2011
 *      Author: hermann-local
 */

#ifndef CPPCLIENT_H_
#define CPPCLIENT_H_

#include <iostream>
#include "zmq.hpp"
#include "stdio.h"
#include "string.h"
#include "json/json.h"


class rexterCppClient
{
public:

  rexterCppClient(std::string zsock_addr);
  ~rexterCppClient();

  // Send request and receive answer from server
  int send_request(const Json::Value &path, const Json::Value &params, const Json::Value &data, Json::Value &answer);

protected:

private:

  // Open and close ZeroMQ socket connection
  int connect(std::string zsock_addr);
  int disconnect();

  // Verbose
  void display_progress();

  bool connected;
  void * zsock;
  void * zcontext;

  Json::FastWriter js_writer;
  Json::Reader     js_reader;

};

#endif /* CPPCLIENT_H_ */
