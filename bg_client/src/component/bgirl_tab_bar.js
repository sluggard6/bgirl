import React, {Component} from 'react';
import {
  Image,
  View,
  TouchableOpacity,
  Text,
  StyleSheet
} from 'react-native';

export default class BgirlTabBar extends Component {

  constructor(props) {
		super(props);
	}

  propTypes: {
    goToPage: React.PropTypes.func, // 跳转到对应tab的方法
    activeTab: React.PropTypes.number, // 当前被选中的tab下标
    tabs: React.PropTypes.array, // 所有tabs集合

    tabNames: React.PropTypes.array, // 保存Tab名称
		tabIconNames: React.PropTypes.array, // 保存Tab图标
		tabActiveIconNames: React.PropTypes.array, // 保存Tab图标
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
            <Image source={{uri: this.props.tabActiveIconNames[i]}} style={styles.image}/>
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
            <Image source={{uri: this.props.tabIconNames[i]}} style={styles.image}/>
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
		height: 96,
	},

	tab: {
		flex: 1,
		justifyContent: 'center',
		alignItems: 'center',
	},

  active_tab: {
		flex: 1,
		justifyContent: 'center',
		alignItems: 'center',
    backgroundColor: '#ff4563'
	},

  image: {
    height: 64,
    width: 44,
    resizeMode: "center"
  },

	tabItem: {
		flexDirection: 'column',
		alignItems: 'center',
    height: 96,
	},
});
