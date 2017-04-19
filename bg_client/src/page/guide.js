import React, { Component } from 'react';

import {
  Image,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  Text,
  Navigator
} from 'react-native';

import Global from '../utils/global';
// import Main from './main'
import TabBarView from './tab_bar_view';


export default class Guide extends Component {

  _onPressButton() {

    this.props.navigator.resetTo({
			component: TabBarView
		})
  }

  render() {
    return (
      <ScrollView
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.contentContainer}
        bounces={false}
        pagingEnabled={true}
        horizontal={true}>
        <Image source={Global.guide.image1} style={styles.backgroundImage} resizeMode={Image.resizeMode.contain} />
        <Image source={Global.guide.image2} style={styles.backgroundImage} resizeMode={Image.resizeMode.contain} />
        <Image source={Global.guide.image3} style={styles.backgroundImage} resizeMode={Image.resizeMode.contain}>
          <TouchableOpacity onPress={this._onPressButton.bind(this)}>
            <Image source={require('../images/start_button.png')} style={{height: 100, width: 100, margin: 150, resizeMode: Image.resizeMode.contain}} />
          </TouchableOpacity>
        </Image>
      </ScrollView>
    )
  }
}

var styles = StyleSheet.create({
  contentContainer: {
    width: Global.size.width*3,
    height: Global.size.height,
  },
  backgroundImage: {
    width: Global.size.width,
    height: Global.size.height,
    flex: 1,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "flex-end",
    margin: 5,
  }
});
