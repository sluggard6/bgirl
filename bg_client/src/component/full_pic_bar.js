import React, {Component} from 'react';
import {
  Image,
  View,
  TouchableOpacity,
  Text,
  StyleSheet
} from 'react-native';

import Global from '../utils/global';

export default class FullPicTabBar extends Component {

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
    if(i == 0) {
      return (
        <Image key={i} source={require('../images/yuan1.png')} style={{height: 20, width: 20, margin: 2, resizeMode: Image.resizeMode.contain,justifyContent: 'center',alignItems: 'center'}}>
          <Text style={{color: "white"}}>1</Text>
        </Image>
      )
    }
    if(i == this.props.tabs.length - 1){
      return (
        <Image key={i} source={require('../images/yuan1.png')} style={{height: 20, width: 20, margin: 2, resizeMode: Image.resizeMode.contain,justifyContent: 'center',alignItems: 'center'}}>
          <Text style={{color: "white"}}>{this.props.tabs.length}</Text>
        </Image>
      )
    }
    if(i == Global.maxView - 1) {
      return (
        <Image key={i} source={require('../images/yuan1.png')} style={{height: 20, width: 20, margin: 2, resizeMode: Image.resizeMode.contain,justifyContent: 'center',alignItems: 'center'}}>
          <Text style={{color: "white"}}>{Global.maxView}</Text>
        </Image>
      )
    }
    if(this.props.activeTab == i){
      return (<Image key={i} source={require('../images/yuan2.png')} style={{height: 10, width: 10, resizeMode: Image.resizeMode.contain}} />)
    }else{
      return (<Image key={i} source={require('../images/yuan1.png')} style={{height: 5, width: 5, margin: 2, resizeMode: Image.resizeMode.contain}} />)
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
    justifyContent: 'center',
    alignItems: 'center',
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
    backgroundColor: '#ff4563',
    padding: 6/Global.pr
	},

  image: {
    height: 64/Global.pr,
    width: 44/Global.pr,
    resizeMode: "contain",
    borderColor: "black"
  },

	tabItem: {
		flexDirection: 'column',
		alignItems: 'center',
	},
});
