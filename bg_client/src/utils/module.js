import React, {Component} from 'react';
import {
  Text
} from 'react-native';


import Banner from '../component/banner'
import TheTwo from '../component/the_two'
import TheThree from '../component/the_three'

export default class Module extends Component {
  constructor(props) {
    super(props);
    this.buildModule = this.buildModule.bind(this)
  }

  buildModule(module) {
    switch(module.category) {
      case "banner":{
        return (
          <Banner data={module.items} navigator={this.props.navigator} />
        );
        break;
      }

      case "the_two":{
        return (
          <TheTwo data={module.items} />
        );
        break;
      }

      case "the_three":{
        return (
          <TheThree data={module.items} />
        );
        break;
      }

      case "title":{
        return (
          <Text>{module.text}</Text>
        );
        break;
      }

      default: {
        return (
          <Banner data={module.items} />
        );
      }
    }
  }

  render() {
    return this.buildModule(this.props.module)
  }
}
