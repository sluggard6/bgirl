import React, {Component} from 'react';
import {
  View,
  Text
} from 'react-native';


import Banner from '../component/banner'
import TheTwo from '../component/the_two'
import TheThree from '../component/the_three'
import FullViewTab from '../page/full_view_tab'
import Channel from '../page/channel'
import Global from './global'
import Application from './application'
import Http from './http'

export default class Module extends Component {
  constructor(props) {
    super(props);
    this.buildModule = this.buildModule.bind(this)
  }

  onPress(componentId, category) {
    this.props.setLoading(true)
    if(category==0){
      url = Application.getUrl(Global.urls.group)+componentId
      Http.httpGet(url, (res)=>{
        this.props.setLoading(false)
        Global.navigator.push({
          component: FullViewTab,
          params: {
            pics: res.pics
          }
        })
      })
    }else if(category==1){
      url = Application.getUrl(Global.urls.channel)+componentId
      Http.httpGet(url, (res)=>{
        this.props.setLoading(false)
        Global.navigator.push({
          component: Channel,
          params: {
            groups: res.groups
          }
        })
      })
    } 
  }

  buildModule(module) {
    switch(module.category) {
      case "banner":{
        return (
          <Banner data={module.items} onPress={this.onPress.bind(this)}/>
        );
      }

      case "the_two":{
        return (
          <TheTwo data={module.items} onPress={this.onPress.bind(this)}/>
        );
      }

      case "the_three":{
        return (
          <TheThree data={module.items} onPress={this.onPress.bind(this)}/>
        );
      }

      case "title":{
        return (
          <View style={{justifyContent: 'center', alignItems: 'center', margin: 10}}>
            <Text style={{fontSize: 20}}>{module.text}</Text>
          </View>
        );
      }

      case "the_two_square":{
        return (
          <TheTwo data={module.items} onPress={this.onPress.bind(this)} square={true}/>
        );
      }

      case "three_circle":{
        return (
          <TheThree data={module.items} onPress={this.onPress.bind(this)} circle={true}/>
        );
      }

      default: {
        return (
          <Separator/>
        );
      }
    }
  }

  render() {
    return this.buildModule(this.props.module)
  }
}

export class Separator extends Component{

  render(){
    return(
      <View style={{height: 10, width: Global.size.width, backgroundColor: "#DFE0E1"}}/>
    )
  }

}