import React from 'react';


export default class Http {

  static httpGet(url, callback, self, error){
    console.log("httpGet running url : " + url)
    fetch(url, {
      method: "GET",
      credentials: "seid"
    }).then((response) => response.json())
      .then((responseData) => {
        // console.log(responseData)
        callback(responseData)
      }).catch((err) => {
        console.log(err);
        if(error){
          error(err)
        }
        console.log(err);
    });
  }
}
