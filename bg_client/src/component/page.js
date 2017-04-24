import React, {Component} from 'react';

import {
  View,
  Text,
  ListView,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  Navigator
} from 'react-native'

import Global from '../utils/global'
import Application from '../utils/application'
import Http from '../utils/http'
import Module from './module'
import Loading from './loading'
import UMNative from '../utils/umeng_native'


export default class Page extends Component {

  constructor(props) {
    super(props);
    this.state = {
      dataSource: null,
      loaded: false,
      loading: false,
    };
    this.fetchData = this.fetchData.bind(this);
  }

  componentWillMount() {
    UMNative.onPageBegin(this.props.pageName)
  }

  componentWillUnmount() {
    UMNative.onPageEnd(this.props.pageName)
  }

  _updateData(responseData){
    this.setState({
      dataSource: responseData.page.modules,
      loaded: true,
    });
  }

  fetchData() {
    Http.httpGet(Application.getUrl(Global.urls.page)+this.props.pageName,this._updateData.bind(this))
  }

  componentDidMount() {
    this.fetchData();
  }

  renderLoadingView() {
    return (<Loading/>)
  }

  _renderItem=({item}) => (
    <Module module={item} setLoading={this.setLoading.bind(this)}/>
  );

  _showLoading(){
    if(this.state.loading){
      return (<Loading/>)
    }
  }

  setLoading(loading){
    this.setState({
      loading: loading
    })
  }

  render() {
    if (!this.state.loaded) {
      return this.renderLoadingView()
    }
    return (
      <View style={styles.container}>
        <FlatList
          data={this.state.dataSource}
          renderItem={this._renderItem}
        />
        {this._showLoading()}
      </View>
    )
  }
}

var styles = StyleSheet.create({

  container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
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
