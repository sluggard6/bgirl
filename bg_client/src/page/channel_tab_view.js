// @flow

import React, { Component } from 'react';

import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity
} from 'react-native'

import ScrollableTabView, {DefaultTabBar, } from 'react-native-scrollable-tab-view';

import TopBar from '../component/top_bar'
import Page from '../component/page'
import Global from '../utils/global'
import Application from '../utils/application'


export default class ChannelTabView extends Component {

  constructor(props) {
		super(props);
		this.state = {
			tabNames: ['主题馆', '品牌馆']
		};
	}


  render() {
    return (
      <View style={styles.container}>
        <TopBar/>
        <ScrollableTabView
          renderTabBar={() => <ChannelTabBar
            tabNames={this.state.tabNames}
          />}
          locked={true}
          tabBarPosition="top">
          <Page tabLabel="zhutiguan" pageName="zhutiguan"/>
          <Page tabLabel="pinpaiguan" pageName="pinpaiguan"/>
        </ScrollableTabView>
      </View>
     
    );
  }

}

class ChannelTabBar extends Component {

  constructor(props) {
    super(props)
  }

  renderTabOption(tab, i) {
    let fontSize = this.props.activeTab == i? {borderColor: "ff4563"} : "18"; // 判断i是否是当前选中的tab，设置不同的颜色
    // const css = this.props.activeTab == i? "sytles.active_tab" : "sytles.tab";
    if(this.props.activeTab == i){
      return (
        <TouchableOpacity onPress={()=>this.props.goToPage(i)} style={styles.active_tab} key={i}>
          <View style={styles.tabItem}>
            <Text style={styles.text}>
              {this.props.tabNames[i]}
            </Text>
          </View>
        </TouchableOpacity>
      );
    }else{
      return (
        <TouchableOpacity onPress={()=>this.props.goToPage(i)} style={styles.tab} key={i}>
          <View style={styles.tabItem}>
            <Text style={{fontSize: 18, color: "#e0e0e0"}}>
              {this.props.tabNames[i]}
            </Text>
          </View>
        </TouchableOpacity>
      );
    }
  }

  render() {
		return (
			<View style={styles.tabs}>
				{this.props.tabs.map((tab, i) => this.renderTabOption(tab, i))}
			</View>
		);
	}

}


const styles = StyleSheet.create({

  container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'flex-start',
    flexWrap: 'nowrap',
    alignItems: 'center',
    backgroundColor: '#333740'
  },

	tabs: {
		flexDirection: 'row',
		height: 140/Global.pr,
	},

	tab: {
		flex: 1,
		justifyContent: 'center',
		alignItems: 'center',
    padding: 6/Global.pr
	},

  active_tab: {
		flex: 1,
		justifyContent: 'center',
		alignItems: 'center',
    padding: 6/Global.pr
	},

  image: {
    height: 64/Global.pr,
    width: 44/Global.pr,
    resizeMode: "contain",
    borderColor: "black"
  },

  text: {
    borderColor: "#ff4563",
    fontSize: 20,
    borderBottomWidth: 2,
    color: "white"
  },

	tabItem: {
		flexDirection: 'column',
		alignItems: 'center',
	},
});
