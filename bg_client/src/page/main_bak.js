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

const PIC_URL = "/pic/list?ids=50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67"
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

  _updateDataSource(responseData){
    const data = this.buildDataSource(responseData.pics);
    this.setState({
      dataSource: this.state.dataSource.cloneWithRows(data),
      loaded: true,
    });
  }

  fetchData() {
    url = Global.default_host + PIC_URL
    Http.httpGet(url,this._updateDataSource.bind(this))
  }

  componentDidMount() {
    this.fetchData();
  }

  buildDataSource(data) {
    if(data instanceof Array){
      if(temp.length > 0) {
        data = temp.concat(data);
        temp = [];
      }
      if(data.lenth % 2 == 1) {
        temp[0] = data.pop();
      }
      let dataSource = new Array();
      let ta = [];
      for(let i=0;i<data.length;i++) {
        if(ta.push(data[i])==2){
          dataSource.push(ta);
          ta = [];
        }
      }
      return dataSource;
    }else{
      throw {
        msg: "错误的参数，data必须是数组",
        value: data
      }
    }
  }

  _renderRow(rowData,sectionID, rowID) {
    return(
      <View style={styles.list_container}>
        <ViewPic
          pic={rowData[0]}
        />
        <ViewPic
          pic={rowData[1]}
        />
      </View>
    );
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
