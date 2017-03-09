// @flow

import React, {Component} from 'react';

import {
  StyleSheet,
  View,
  Image,
  Text,
  TouchableOpacity
} from 'react-native';

export default class TimerButton extends Component {

  constructor(props) {
		super(props);
    this.state={
      isDisabled: false,
      seconds: this.props.disTime
    }
	}

  componentWillUnmount() {
    clearInterval(this.interval)
  }

  onPress(call){
    if(this.state.isDisabled == false) {
      this.setState({
        isDisabled: true
      })
      call();
      this.interval = setInterval(() => {
        if(this.state.seconds <= 0) {
          clearInterval(this.interval)
          this.setState({
            seconds: this.props.disTime,
            isDisabled: false
          })
        } else {
          this.setState({
            seconds: (this.state.seconds - 1)
          })
        }
      }, 1000);
    }
  }

  render() {
    const view_text = this.state.isDisabled?this.props.disText + "(" + this.state.seconds + ")":this.props.text
    const btn_style = this.state.isDisabled?this.props.disStyle:this.props.style
    return (
      <TouchableOpacity onPress={()=>this.onPress(this.props.call)} disabled={this.state.isDisabled}>
        <View style={btn_style}>
          <Text style={this.props.textStyle}>{view_text}</Text>
        </View>
      </TouchableOpacity>
    )
  }
}
