import React, {Component} from 'react';
import {
  Image,
  View,
  TouchableOpacity,
  Text,
  StyleSheet
} from 'react-native';

import Global from '../utils/global';

export default class BgirlTabBar extends Component {

  constructor(props) {
		super(props);
	}

  setAnimationValue({value}) {
	}

  componentDidMount() {
		// Animated.Value监听范围 [0, tab数量-1]
		this.props.scrollValue.addListener(this.setAnimationValue);
	}

  renderTabOption(tab, i) {
    const color = this.props.activeTab == i? "white" : "black"; // 判断i是否是当前选中的tab，设置不同的颜色
    // const css = this.props.activeTab == i? "sytles.active_tab" : "sytles.tab";
    if(this.props.activeTab == i){
      return (
        <TouchableOpacity onPress={()=>this.props.goToPage(i)} style={styles.active_tab} key={i}>
          <View style={styles.tabItem}>
            <Image source={this.props.tabActiveIconNames[i]} style={styles.image}/>
            <Text style={{color: color}}>
              {this.props.tabNames[i]}
            </Text>
          </View>
        </TouchableOpacity>
      );
    }else{
      return (
        <TouchableOpacity onPress={()=>this.props.goToPage(i)} style={styles.tab} key={i}>
          <View style={styles.tabItem}>
            <Image source={this.props.tabIconNames[i]} style={styles.image}/>
            <Text style={{color: color}}>
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
	tabs: {
		flexDirection: 'row',
		height: 50,
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
    backgroundColor: '#ff4563',
    padding: 6/Global.pr
	},

  image: {
    height: 25,
    width: 18,
    resizeMode: "contain",
    borderColor: "black"
  },

	tabItem: {
		flexDirection: 'column',
		alignItems: 'center',
	},
});
