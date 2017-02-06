import React, {Component} from 'react';

import {
  View,
  Text,
  ListView,
  StyleSheet,
  Navigator
} from 'react-native'

import ViewPic from '../component/view_pic'

var pic_data = [
	{title:'第一张', date:'2017-01-03', path:{max:'../image/max.jpg',normal:'../image/normal.jpg',min:'../image/min.jpg'}},
	{title:'第二张', date:'2017-01-03', path:{max:'../image/max.jpg',normal:'../image/normal.jpg',min:'../image/min.jpg'}},
	{title:'第三张', date:'2017-01-03', path:{max:'../image/max.jpg',normal:'../image/normal.jpg',min:'../image/min.jpg'}},
	{title:'第四张', date:'2017-01-03', path:{max:'../image/max.jpg',normal:'../image/normal.jpg',min:'../image/min.jpg'}},
	{title:'第五张', date:'2017-01-03', path:{max:'../image/max.jpg',normal:'../image/normal.jpg',min:'../image/min.jpg'}},
	{title:'第六张', date:'2017-01-03', path:{max:'../image/max.jpg',normal:'../image/normal.jpg',min:'../image/min.jpg'}},
	{title:'第七张', date:'2017-01-03', path:{max:'../image/max.jpg',normal:'../image/normal.jpg',min:'../image/min.jpg'}},
	{title:'第八张', date:'2017-01-03', path:{max:'../image/max.jpg',normal:'../image/normal.jpg',min:'../image/min.jpg'}}
]

let temp = [];

export default class Main extends Component {

  constructor(props) {
    super(props);
    const ds = new ListView.DataSource({rowHasChanged: (r1, r2) => r1 !== r2});
    this.state = {
      dataSource: ds.cloneWithRows(this.buildDataSource(pic_data))
    };
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
      <View style={styles.container}>
        <ViewPic
          data={rowData[0]}
        />
        <ViewPic
          data={rowData[1]}
        />
      </View>
    );
  }


  render() {
    return (
      <View style={{flex: 1, paddingTop: 22}}>
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
    flexDirection: 'row',
    justifyContent: 'space-around',
    flexWrap: 'nowrap',
    alignItems: 'center',
    padding: 5,
  },

});
