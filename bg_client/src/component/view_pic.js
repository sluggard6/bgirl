import React, {Component} from 'react';

import {
  StyleSheet,
  View,
  Image,
  Text
} from 'react-native'

export default class ViewPic extends Component {

  constructor(props) {
    super(props);
  }

  render(){
    return (
      <View style={styles.container}>
        <Image
          source={require('../images/min.jpg')}
        />
        <Text>{this.props.data.title}</Text>
        <Text>{this.props.data.date}</Text>
      </View>
    );
  }
}

var styles = StyleSheet.create({

  container: {
    flex: 1,
    flexDirection: "column",
    justifyContent: 'space-around',
    alignItems: 'center',
    padding: 5,
  }
})
