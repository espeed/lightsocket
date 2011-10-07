/*
 * main.cpp
 *
 *  Created on: 04.10.2011
 *      Author: hermann-local
 */

#include "rexterCppClient.h"

int main(int argc, const char *argv[])
{

  rexterCppClient* client = new rexterCppClient("tcp://localhost:5555");

  Json::Value js_data(Json::objectValue);
  Json::Value js_params(Json::objectValue);
  Json::Value js_answer;

  Json::Value js_path("wordgraph/vertices/create");
  js_data["city"] = "Dallas";
  js_data["name"] = "Frank";


  for( int i = 0; i < 1; i++)
  {
    js_data["counter"] = i;
    client->send_request(js_path, js_params, js_data, js_answer);
  }
  delete client;

  return 0;
}


