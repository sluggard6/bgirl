import React, {Component} from 'react';
import {
  Text
} from 'react-native';


import Banner from '../component/banner'
import ViewPic from '../component/view_pic'

export default class Module extends Component {
  constructor(props) {
    super(props);
    this.buildModule = this.buildModule.bind(this)
  }

  buildModule(module) {
    switch(module.category) {
      case "banner":{
        return (
          <Banner data={module.items} />
        );
        break;
      }

      case "the_two":{
        return (
          <ViewPic data={module.items} />
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
