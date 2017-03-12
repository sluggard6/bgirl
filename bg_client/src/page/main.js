import React, {Component} from 'react';

import {
  View,
  Text,
  ListView,
  StyleSheet,
  Navigator
} from 'react-native'

import ViewPic from '../component/view_pic'
import Global from '../utils/global'
import Http from '../utils/http'
import TopBar from '../component/top_bar'
import Module from '../utils/module'

const PIC_URL = "/page/index"
// const PIC_URL = "http://192.168.161.35:8290/pic/list?ids=1,2"

let temp = [];

export default class Main extends Component {

  constructor(props) {
    super(props);
    this.state = {
      dataSource: new ListView.DataSource({rowHasChanged: (r1, r2) => r1 !== r2}),
      loaded: false
    };
    this.fetchData = this.fetchData.bind(this);
  }

  _updateData(responseData){
    console.log(responseData.page.modules.length)
    this.setState({
      dataSource: this.state.dataSource.cloneWithRows(responseData.page.modules),
      loaded: true,
    });
  }

  fetchData() {
    url = Global.default_host + PIC_URL
    Http.httpGet(url,this._updateData.bind(this))
  }

  componentDidMount() {
    this.fetchData();
  }

  renderLoadingView() {
    return (
      <View style={styles.container}>
        <Text>
          正在加载数据……
        </Text>
      </View>
    );
  }

  _renderRow(rowData,sectionID, rowID) {
    console.log("row_id:" + rowData.id)
    return(
      <Module module={rowData} navigator={this.props.navigator}/>
    );
  }

  render() {
    if (!this.state.loaded) {
      return this.renderLoadingView();
    }
    return (
      <View style={styles.container}>
        <TopBar/>
        <ListView
          dataSource={this.state.dataSource}
          renderRow={this._renderRow.bind(this)}
        />
      </View>
    )
  }
}

var styles = StyleSheet.create({

  container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'flex-start',
    flexWrap: 'nowrap',
    alignItems: 'center',
    backgroundColor: '#DFE0E1'
  },

  list_container: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-around',
    flexWrap: 'nowrap',
    alignItems: 'center',
    width: Global.size.width
  },

});
