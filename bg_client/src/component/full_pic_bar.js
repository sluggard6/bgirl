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

  propTypes: {
    goToPage: React.PropTypes.func, // 跳转到对应tab的方法
    activeTab: React.PropTypes.number, // 当前被选中的tab下标
    tabs: React.PropTypes.array, // 所有tabs集合
  }

  setAnimationValue({value}) {
	}

  componentDidMount() {
		// Animated.Value监听范围 [0, tab数量-1]
		this.props.scrollValue.addListener(this.setAnimationValue);
	}

  renderTabOption(tab, i) {
    if(this.props.activeTab == i){
      return (<Text key={i}>{i+1}</Text>)
    }
    return;
  }

  render() {
		return (
			<View style={styles.tabs}>
        <Text>1...</Text>
        {this.props.tabs.map((tab, i) => this.renderTabOption(tab, i))}
        <Text>...{this.props.tabs.length}</Text>
			</View>
		);
	}
}


const styles = StyleSheet.create({
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
