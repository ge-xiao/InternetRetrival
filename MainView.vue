<template>
  <div style="padding: 32px">
    <div style="margin-top: 10%">
      <div>
        <img :src="logo"/>
      </div>

      <el-radio-group v-model="mode" >
        <el-radio label='0' >bool查询</el-radio>
        <el-radio label='1' >zone查询</el-radio>
        <el-radio label='2' >模糊查询</el-radio>
        <el-radio label='3' >排名查询</el-radio>
        <!--          <el-radio :label="3" >系统自带</el-radio>-->
      </el-radio-group>

      <div style="margin-top: 10px" v-if="mode=='0'">
        <el-input
            class="input"
            :rows="10"
            style="width: 60%;"
            @keyup.enter.native="search(text,0)"
            placeholder="请输入"
            prefix-icon="el-icon-search"
            v-model="text">
        </el-input>
      </div>

      <div style="margin-top: 10px" v-if="mode=='1'">
        <div style="margin-bottom: 10px">
          <span class="my-span">题目</span><el-input style="width: 200px" v-model="form.title"> </el-input>
        </div>
        <div style="margin-bottom: 10px">
          <span class="my-span">作者</span>  <el-input style="width: 200px" v-model="form.author"> </el-input>
        </div>
        <div style="margin-bottom: 10px">
          <span class="my-span">朝代</span> <el-input style="width: 200px" v-model="form.dynasty"> </el-input>
        </div>
        <div style="margin-bottom: 10px">
          <span class="my-span">内容</span>  <el-input style="width: 200px" v-model="form.content"> </el-input>
        </div>

        <el-button @click="search('',1)">搜索</el-button>

      </div>

      <div style="margin-top: 10px" v-if="mode=='2'">
        <el-input
            class="input"
            :rows="10"
            style="width: 60%;"
            @keyup.enter.native="search(text,2)"
            placeholder="请输入"
            prefix-icon="el-icon-search"
            v-model="text">
        </el-input>
      </div>

      <div style="margin-top: 10px" v-if="mode=='3'">
        <el-input
            class="input"
            :rows="10"
            style="width: 60%;"
            @keyup.enter.native="search(text,3)"
            placeholder="请输入"
            prefix-icon="el-icon-search"
            v-model="text">
        </el-input>
      </div>
      <div style="
        margin-top: 30px">

        <el-card v-for="(item,index) in viewTableData"  style="width: 60%;margin: 0 auto">
          <span style="font-weight: bold;font-size: 20px"> &laquo{{item.title}}&raquo </span>
          <div>
            <span style="color: #999999;font-size: 10px">{{item.author}}. </span>
            <span style="color: #999999;font-size: 10px">{{item.dynasty}}</span>
          </div>
          <div>

          </div>
          <div>
            <span>{{item.content}}</span>
          </div>
          <div style="text-align: right">

            {{item.favor}}

              <svg class="icon" aria-hidden="true" style="font-size:25px;cursor: pointer" @click="dianzan(item.index,index)">
                <use xlink:href="#icon-icon"></use>
              </svg>

          </div>
        </el-card>


        <el-pagination
            v-if="this.totalLength>0"
            background
            layout="prev, pager, next"
            :page-size="pagesize"
            :total="totalLength"
            @current-change="change">
        </el-pagination>
      </div>

    </div>
  </div>
</template>

<script>

import request from "@/utils/request";

export default {
  name: "MainView",
  created() {
    this.load();
  },

  data() {
    return {
      tableData: [],
      viewTableData:[],
      totalLength:0,
      pagesize:10,
      logo:require("../assets/logo.png"),
      text:"",
      mode:"0",
      form:{
        title:"",
        author:"",
        dynasty:"",
        content:""
      },

    }
  },
  methods: {
    load(){

    },
    change(cur){
      console.log(cur)
      this.viewTableData=this.tableData.slice(this.pagesize*(cur-1),this.pagesize*(cur))
      document.documentElement.scrollTop = 0;
    },

    search(text,ch){
      //this.text=""
      if(ch==0){
        request.get("flask/boolQuery",{params:{
            str:text
          }}).then(res=>{
          console.log(res)
          this.tableData=res
          this.totalLength=this.tableData.length
          this.viewTableData=this.tableData.slice(0,this.pagesize)
        })
      }else if(ch==2){
        request.get("flask/fuzzySearch",{params:{
            str:text
          }}).then(res=>{
          console.log(res)
          this.tableData=res
          this.totalLength=this.tableData.length
          this.viewTableData=this.tableData.slice(0,this.pagesize)

        })
      }else if(ch==1){
        request.get("flask/zoneSpecificQuery",{params:this.form}).then(res=>{
          console.log(res)
          this.tableData=res
          this.totalLength=this.tableData.length
          this.viewTableData=this.tableData.slice(0,this.pagesize)
        })
        // for(let k in this.form){
        //   this.form[k]=""
        // }
      }else if(ch==3){

        request.get("flask/rankedsearch",{params:{
            str:text
          }}).then(res=>{
          console.log(res)
          this.tableData=res
          this.totalLength=this.tableData.length
          this.viewTableData=this.tableData.slice(0,this.pagesize)
        })

      }
    },

    dianzan(index,tableIndex){
      request.get("flask/dianzan",{params:{
          index:index
        }}).then(res=>{
        this.viewTableData[tableIndex].favor+=1;
      })

    },
  }
}
</script>

<style >
.my-span{
  margin-right: 20px;
}
.el-card__body, .el-main{
  padding: 10px;
}

.input .el-input__icon{
  line-height: 50px !important;
}
.input .el-icon-search:before {
  font-size: 25px !important;
}
.el-input--prefix .el-input__inner{
  padding-left: 50px !important;
}
.input .el-input__inner{
  height: 50px !important;
  border-radius: 30px !important;
  font-size: 15px !important;
}
</style>