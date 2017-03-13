import React from 'react';


export default class Http {

  static httpGet(url, callback, self, error){
    // console.log(url+"*******************");
    fetch(url, {
      method: "GET",
      credentials: "seid"
    }).then((response) => response.json())
      .then((responseData) => {
        callback(responseData)
      }).catch((err) => {
        console.log(err);
        if(error){
          error(err)
        }
        console.log(err);
    });
  }

  static httpPost(url, params, callback, self, error){
    body = Http.json2form(params)
    fetch(url, {
      method: "POST",
      credentials: "seid",
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: body
    }).then((response) => response.json())
      .then((responseData) => {
        console.log(responseData)
        callback(responseData)
      }).catch((err) => {
        console.log(err);
        if(error){
          error(err)
        }
        console.log(err);
    });
  }

  static json2form(params){
    let body = []
    for(let key in params) {
      body.push(key + "=" + params[key])
    }
    return body.join("&")
  }
}
