import React from 'react';


export default class Http {

  static async httpGet(url, callback, self, error){
    // console.log(url+"*******************");
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
