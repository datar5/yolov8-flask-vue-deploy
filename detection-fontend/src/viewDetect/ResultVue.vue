<template>
  <div class="container">
    <div>
      <div class="content-title">模型信息</div>
      <div class="handle-box">
        <el-input v-model="model_query.keyword" placeholder="模型名称" class="handle-input mr10"></el-input>
        <el-button type="primary" :icon="Search " @click="handleModelSearch">搜索</el-button>

        <el-button type="success"  @click="handleModelAll">
          <el-icon><List /></el-icon>
          <span>列出模型</span>
        </el-button>
      </div>


      <el-table :data="modelData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
        <el-table-column prop="wid" label="模型ID" width="55" align="center"></el-table-column>
        <el-table-column prop="model_name" label="文件名"></el-table-column>


        <el-table-column prop="model_type" label="模型类别"></el-table-column>
        <el-table-column prop="model_dataset" label="对应数据集"></el-table-column>


<!--        <el-table-column label="操作" width="300" align="center">-->
<!--          <template #default="scope">-->
<!--            <el-button text :icon="Search" class="green" @click="handleModelDetail(scope.$index, scope.row)" v-permiss="15">-->
<!--              查看-->
<!--            </el-button>-->
<!--          </template>-->
<!--        </el-table-column>-->
      </el-table>

      <div class="pagination">
        <el-pagination
            background
            layout="total, sizes, prev, pager, next, jumper"
            v-model:current-page="model_query.curPage"
            v-model:page-size="model_query.pageSize"

            :page-sizes="[5, 10]"
            :total="modelTotal"
            @current-change="handleModelPageChange"
            @size-change="handleModelSizeChange"

        ></el-pagination>
      </div>
    </div>


    <div class="content-title">图片查看</div>
    <div class="handle-box">
      <el-input v-model="query.keyword" placeholder="文件名称" class="handle-input mr10"></el-input>
      <el-button type="primary" :icon="Search " @click="handleSearch">搜索</el-button>

<!--      <el-button type="primary"  @click="getData">-->
<!--        <el-icon><Refresh /></el-icon>-->
<!--        <span>刷新页面</span>-->
<!--      </el-button>-->

      <el-button type="success"  @click="handleAll">
        <el-icon><List /></el-icon>
        <span>列出全部</span>
      </el-button>
    </div>

    <el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
      <el-table-column prop="fid" label="文件ID" width="55" align="center"></el-table-column>
      <el-table-column prop="name" label="文件名"></el-table-column>

      <el-table-column label="图片(查看大图)" align="center">
        <template #default="scope">
          <el-image
              class="table-td-thumb"
              :src="scope.row.img_url"
              :z-index="10"
              :preview-src-list="[scope.row.img_url]"
              preview-teleported
          >
          </el-image>
        </template>
      </el-table-column>

      <el-table-column label="时间">
        <template #default="scope">{{ scope.row.timestamp }}</template>
      </el-table-column>

      <el-table-column prop="type" label="文件类别"></el-table-column>
      <el-table-column prop="origin" label="文件来源"></el-table-column>
      <el-table-column prop="width" label="宽度"></el-table-column>
      <el-table-column prop="height" label="高度"></el-table-column>

    </el-table>

    <div class="pagination">
      <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          v-model:current-page="query.curPage"
          v-model:page-size="query.pageSize"

          :page-sizes="[5, 10]"
          :total="pageTotal"
          @current-change="handlePageChange"
          @size-change="handleSizeChange"

      ></el-pagination>
    </div>

    <div class="content-title">记录管理</div>

    <div class="handle-box">
      <el-input v-model="result_query.keyword" placeholder="结果名称" class="handle-input mr10"></el-input>
      <el-button type="primary" :icon="Search " @click="handleResultSearch">搜索</el-button>

      <el-button type="success"  @click="handleResultAll">
        <el-icon><List /></el-icon>
        <span>列出结果</span>
      </el-button>
    </div>

    <el-table :data="resultData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
      <el-table-column prop="rid" label="结果ID" width="55" align="center"></el-table-column>
      <el-table-column prop="wid" label="模型ID"></el-table-column>

      <el-table-column label="图片(查看大图)" align="center">
        <template #default="scope">
          <el-image
              class="table-td-thumb"
              :src="scope.row.img_url"
              :z-index="10"
              :preview-src-list="[scope.row.img_url]"
              preview-teleported
          >
          </el-image>
        </template>
      </el-table-column>

      <el-table-column label="时间">
        <template #default="scope">{{ dateForm(scope.row.timestamp) }}</template>
      </el-table-column>

      <el-table-column prop="type" label="文件类别"></el-table-column>
      <el-table-column prop="addition" label="额外说明"></el-table-column>
      <el-table-column prop="mission_type" label="任务类型"></el-table-column>
      <el-table-column prop="filename" label="文件来源"></el-table-column>
      <el-table-column prop="num" label="检测数目"></el-table-column>

      <el-table-column label="操作" width="300" align="center">
        <template #default="scope">
          <el-button text :icon="TopLeft" class="primary" @click="handleResultDetail(scope.row)" v-permiss="15">
            查看
          </el-button>
          <el-button text :icon="Edit" @click="handleResultEdit(scope.row)" v-permiss="15">
            编辑
          </el-button>
          <el-button text :icon="Delete" class="red" @click="handleResultDelete(scope.row)" v-permiss="16">
            删除
          </el-button>
        </template>
      </el-table-column>

    </el-table>

    <div class="pagination">
      <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          v-model:current-page="result_query.curPage"
          v-model:page-size="result_query.pageSize"

          :page-sizes="[5, 10]"
          :total="resultTotal"
          @current-change="handleResultPageChange"
          @size-change="handleResultSizeChange"

      ></el-pagination>
    </div>

    <el-dialog title="结果编辑" v-model="resultEditVisible" width="30%">
      <el-form label-width="100px">
        <el-form-item label="结果ID">
          <span>{{resultEditForm.rid}}</span>
        </el-form-item>

        <el-form-item label="模型ID">
          <span>{{resultEditForm.wid}}</span>
        </el-form-item>

        <el-form-item label="时间">
          <span>{{ dateForm(resultEditForm.timestamp) }}</span>
        </el-form-item>

        <el-form-item label="文件类别">
          <span>{{resultEditForm.type}}</span>
        </el-form-item>


        <el-form-item label="额外说明">
          <el-input v-model="resultEditForm.addition"></el-input>
        </el-form-item>

        <el-form-item label="任务类别">
          <el-input v-model="resultEditForm.mission_type"></el-input>
        </el-form-item>

        <el-form-item label="检测数目">
          <span>{{ resultEditForm.num }}</span>
        </el-form-item>

      </el-form>
      <template #footer>
          <span class="dialog-footer">
            <el-button @click="submitEdit" type="primary">提交</el-button>
            <el-button @click="resultEditVisible = false" >退出</el-button>
          </span>
      </template>
    </el-dialog>

    <el-dialog title="结果细节" v-model="objDetail" width="70%" class="content-title">

      <div class="content-title">原图显示</div>
      <div class="demo-image__lazy">
        <el-image v-for="url in [obj_query.img_url]"  :key="url" :src="url" lazy />
      </div>

      <div class="content-title">任务信息</div>
      <el-descriptions :column="3" border>
        <el-descriptions-item
            label="时间"
            label-align="right"
            align="center"
            label-class-name="my-label"
            class-name="my-content"
            width="200px">
          {{dateForm(resultParams.timestamp)}}
        </el-descriptions-item>

        <el-descriptions-item label="文件类别" label-align="right" align="center" width="100px">
          {{resultParams.type}}
        </el-descriptions-item>
        <el-descriptions-item label="额外说明" label-align="right" align="center">
          {{resultParams.addition}}
        </el-descriptions-item>

        <el-descriptions-item label="任务类型" label-align="right" align="center">
          <el-tag size="large" type="success">
          {{resultParams.mission_type}}
          </el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="文件来源" label-align="right" align="center">
          {{resultParams.filename}}
        </el-descriptions-item>
      </el-descriptions>

      <div class="content-title">检测模型</div>

      <el-descriptions :column="3" border>
        <el-descriptions-item
            label="模型ID"
            label-align="right"
            align="center"
            label-class-name="my-label"
            class-name="my-content"
            width="150px">
          {{model_params.wid}}
        </el-descriptions-item>

        <el-descriptions-item label="文件名" label-align="right" align="center">
          {{model_params.model_name}}
        </el-descriptions-item>
        <el-descriptions-item label="模型类别" label-align="right" align="center">
          <el-tag size="middle" type="primary">{{model_params.model_type}}</el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="对应数据集" label-align="right" align="center">
          {{model_params.model_dataset}}
        </el-descriptions-item>
      </el-descriptions>

      <div class="content-title">物体细节</div>

      <el-table :data="objData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
        <el-table-column prop="oid" label="物体ID"></el-table-column>
        <el-table-column prop="rid" label="结果ID"></el-table-column>
        <el-table-column prop="cls" label="类别"></el-table-column>
        <el-table-column prop="conf" label="置信度"></el-table-column>
        <el-table-column prop="x1" label="左上角横坐标"></el-table-column>
        <el-table-column prop="y1" label="左上角纵坐标"></el-table-column>
        <el-table-column prop="x2" label="右下角横坐标"></el-table-column>
        <el-table-column prop="y2" label="右下角纵坐标"></el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
            background
            layout="total, sizes, prev, pager, next, jumper"
            v-model:current-page="obj_query.curPage"
            v-model:page-size="obj_query.pageSize"

            :page-sizes="[5, 10, 20]"
            :total="objTotal"
            @current-change="handleObjPageChange"
            @size-change="handleObjSizeChange"

        ></el-pagination>
      </div>

      <template #footer>
          <span class="dialog-footer">
            <el-button @click="objDetail = false" >退出</el-button>
          </span>
      </template>
    </el-dialog>

  </div>

</template>

<script lang="ts" setup>
import {ref, reactive, onMounted} from 'vue';
import {ElMessage, ElMessageBox, FormRules} from 'element-plus';
import {Delete, Edit, Search, Plus, TopLeft} from '@element-plus/icons-vue';
import axios from "axios";
import {compileScript} from "@vue/compiler-sfc";
// import { fetchData } from '../api/index';

interface TableItem { // 定义图片的泛型

  // id: number;
  // name: string;
  // money: string;
  // state: string;
  // date: string;
  // address: string;
  fid: number;
  height: number;
  width: number;
  origin: string;
  timestamp:string;
  type: string;
  name: string;
  img_url: string;
}

interface ModelItem{ // 定义model的接口
  wid: number,
  model_name: string,
  model_type: string,
  model_dataset: string
}

interface ResultItem{ // 定义model的接口
  rid: number,
  wid: number,
  timestamp: number
  type: string,
  addtion: string,
  mission_type: string,
  filename: string,
  num: number
}

interface ObjItem{ // 定义model的接口
  oid: number,
  rid: number,
  cls: string,
  x1: number,
  y1: number,
  x2: number,
  y2: number,
  conf: number
}

// 下面定义的是file表相关的数据
const query = reactive({
  curPage: 1,
  pageSize: 5,
  tableName: "file",
  keyword: ""
});

const tableData = ref<TableItem[]>([]);  // 表格数据

const pageTotal = ref(0);

// 下面定义的是model表相关的数据
const model_query = reactive({
  curPage: 1,
  pageSize: 5,
  tableName: "model",
  keyword: ""
})

const modelData = ref<ModelItem[]>([])
const modelTotal = ref(0)

// 下面定义的是result表的相关的数据
const result_query = reactive({
  curPage: 1,
  pageSize: 5,
  tableName: "result",
  keyword: ""
})

const resultData = ref<ResultItem[]>([])
const resultTotal = ref(0)


// 获取file表格数据
const getData = () => {
  // console.log(query)

  if(query.keyword.length == 0){
    axios({
      method: 'GET',
      url: '/page',
      params: {
        curPage: query.curPage,
        pageSize: query.pageSize,
        tableName: "file"
      },
    }).then(res=>{
      tableData.value= res.data.results
      // console.log(tableData)
    })

    axios({
      method: 'GET',
      url: '/num',
      params: {
        tableName: "file",
        rid: -2
      },
    }).then(res=>{
      pageTotal.value= res.data.results
    })
  }
  else{
    axios({
      method: 'GET',
      url: '/deblurS',
      params: {
        curPage: query.curPage,
        pageSize: query.pageSize,
        keyword: query.keyword,
        tableName: "file"
      },
    }).then(res=>{
      // console.log(res)
      tableData.value= res.data.results
      // console.log(tableData)
    })

    axios({
      method: 'GET',
      url: '/deblurSNum',
      params: {
        keyword: query.keyword,
        tableName: "file"
      },
    }).then(res=>{
      pageTotal.value= res.data.results
    })
  }
};

// 获得model表格的数据
const getModelData = () => {
  if(model_query.keyword.length == 0){
    axios({
      method: 'GET',
      url: '/page',
      params: {
        curPage: model_query.curPage,
        pageSize: model_query.pageSize,
        tableName: "model"
      },
    }).then(res=>{
      modelData.value= res.data.results
      // console.log(tableData)
    })

    axios({
      method: 'GET',
      url: '/num',
      params: {
        tableName: "model",
        rid: -2
      },
    }).then(res=>{
      modelTotal.value= res.data.results
    })
  }
  else{
    axios({
      method: 'GET',
      url: '/deblurS',
      params: {
        curPage: model_query.curPage,
        pageSize: model_query.pageSize,
        keyword: model_query.keyword,
        tableName: "model"
      },
    }).then(res=>{
      // console.log(res)
      modelData.value= res.data.results
      // console.log(tableData)
    })

    axios({
      method: 'GET',
      url: '/deblurSNum',
      params: {
        keyword: model_query.keyword,
        tableName: "model"
      },
    }).then(res=>{
      modelTotal.value= res.data.results
    })
  }
}

const getResultData = () => {
  if(result_query.keyword.length == 0){
    axios({
      method: 'GET',
      url: '/page',
      params: {
        curPage: result_query.curPage,
        pageSize: result_query.pageSize,
        tableName: "result"
      },
    }).then(res=>{
      resultData.value= res.data.results
      // console.log(tableData)
    })

    axios({
      method: 'GET',
      url: '/num',
      params: {
        tableName: "result",
        rid: -2
      },
    }).then(res=>{
      resultTotal.value= res.data.results
    })
  }
  else{
    axios({
      method: 'GET',
      url: '/deblurS',
      params: {
        curPage: result_query.curPage,
        pageSize: result_query.pageSize,
        keyword: result_query.keyword,
        tableName: "result"
      },
    }).then(res=>{
      // console.log(res)
      resultData.value= res.data.results
      // console.log(tableData)
    })

    axios({
      method: 'GET',
      url: '/deblurSNum',
      params: {
        keyword: result_query.keyword,
        tableName: "result"
      },
    }).then(res=>{
      resultTotal.value= res.data.results
    })
  }
}


onMounted(() => {
  getData()
  getModelData()
  getResultData()
})

// 下面的分页get得到数据操作是针对的file表
// 模糊查找操作
const handleSearch = () => {
  query.curPage = 1;
  getData();
};
// 列出全部
const handleAll = () => {
  query.keyword = '';
  query.curPage = 1
  getData();
}

// 分页导航
const handlePageChange = (val: number) => {
  query.curPage = val;
  getData();
};

const handleSizeChange  = (val: number) => {
  query.pageSize = val;
  getData();
};

// 下面的分页get得到数据操作是针对的model表
// 模糊查找操作
const handleModelSearch = () => {
  model_query.curPage = 1;
  getModelData();
};

// 列出全部
const handleModelAll = () => {
  model_query.keyword = '';
  model_query.curPage = 1
  getModelData();
}

// 分页导航
const handleModelPageChange = (val: number) => {
  model_query.curPage = val;
  getModelData();
};

const handleModelSizeChange  = (val: number) => {
  model_query.pageSize = val;
  getModelData();
};


// 下面的分页get得到数据操作是针对的result表

const dateForm = (originVal: number) => {  // 时间戳转日期
      var now = new Date(originVal * 1000)
      var y = now.getFullYear()
      var m = now.getMonth() + 1
      var d = now.getDate()
      return  y + "-" + (m < 10 ? "0" + m : m) + "-" +
          (d < 10 ? "0" + d : d) + " " + now.toTimeString().substr(0, 8);
}


const handleResultSearch = () => {
  result_query.curPage = 1;
  getResultData();
};

// 列出全部
const handleResultAll = () => {
  result_query.keyword = '';
  result_query.curPage = 1
  getResultData();
}

// 分页导航
const handleResultPageChange = (val: number) => {
  result_query.curPage = val;
  getResultData();
};

const handleResultSizeChange  = (val: number) => {
  result_query.pageSize = val;
  getResultData();
};

/***
 记录相关操作
 ***/
const resultEditVisible = ref(false)
const resultEditForm = reactive({
  rid: -1,
  wid: -1,
  timestamp: '',
  type: '',
  addition: '',
  mission_type: '',
  filename: '',
  num: -1
})

const handleResultEdit = (row: any) => {
  for(var key in row){
    resultEditForm[key] = row[key]
  }
  resultEditVisible.value = true
}

const submitEdit = () => {
  resultEditVisible.value = false
  axios({
    method: 'PUT',
    url: '/result/' + resultEditForm.rid,
    data: resultEditForm
  }).then(res=>{
    console.log(res)
    if(res.data.status == 'success'){
      ElMessage.success('修改成功')
      getResultData()
    }
  })
}


/**
 * 显示物体信息细节
 */

// 下面定义的是obj表的相关数据
const obj_query = reactive({
  curPage: 1,
  pageSize: 5,
  tableName: "obj",
  rid: 1
})

const model_params = reactive({
  model_dataset: null,
  model_name: null,
  model_type: null,
  wid: -1
})

const resultParams = reactive({
  timestamp: "",
  type: "",
  addition: "",
  mission_type: "",
  filename: ""
})

const objData = ref<ObjItem[]>([])
const objTotal = ref(0)
const objDetail = ref(false)

const handleResultDetail = (row: any) => {
  objDetail.value = true
  for(var key in row){
    obj_query[key] = row[key]
    resultParams[key] = row[key]
  }
  axios({
    method: 'GET',
    url: '/wmodel/' + row.wid
  }).then(res=>{
    for(var key in res.data.results){
      model_params[key] = res.data.results[key]
    }
  })
  getResultDetail(row)
  objTotal.value = row.num
  // console.log(row.rid)
  // console.log({
  //   'curPage': obj_query.curPage,
  //   'pageSize': obj_query.pageSize
  // })
}

const getResultDetail = () => {
  axios({
    method: 'GET',
    url: '/objectPage/' + obj_query.rid,
    params:{
      'curPage': obj_query.curPage,
      'pageSize': obj_query.pageSize
    }
  }).then(res=>{
    objData.value = res.data.results
    for(var i = 0;i < objData.value.length;i++){
      objData.value[i].conf = objData.value[i].conf.toFixed(3)
      // console.log('114514')
    }
  })
}

const handleObjPageChange = (val: number) => {
  obj_query.curPage = val;
  getResultDetail()
};

const handleObjSizeChange  = (val: number) => {
  obj_query.pageSize = val;
  getResultDetail()
};

const handleResultDelete = (row: any) =>{
  ElMessageBox.confirm('确定要删除记录吗？', '提示', {
    type: 'warning'
  }).then(()=>{
    axios({
      method: 'DELETE',
      url: '/obj/' + row.rid
    }).then(res=>{
      if(res.data.status == 'success'){
        axios({
          method: 'DELETE',
          url: '/result/' + row.rid  // 删除的文件操作和删除的数据操作是耦合的
        }).then(res=>{
          if(res.data.status == 'success'){
            ElMessage.success('记录删除成功')
            getResultData()
          }
          else{
            ElMessage.error('记录删除出现异常')
          }
        })
      }
      else{
        ElMessage.error('记录删除出现异常')
      }
    })
  })
}

// 查看模型的内部细节
const handleModelDetail = (index: number, row: any) =>{

}



</script>

<style scoped>
.content-title {
  font-weight: 400;
  line-height: 50px;
  margin: 10px 0;
  font-size: 22px;
  color: #1f2f3d;
}
.upload-demo {
  width: 360px;
}

.handle-box {
  margin-bottom: 20px;
}

.handle-select {
  width: 120px;
}

.handle-input {
  width: 300px;
}
.table {
  width: 100%;
  font-size: 14px;
}
.red {
  color: red;
}

.primary{
  color: cornflowerblue;
}

.green{
  color: green;
}

.blue{
  color: aquamarine;
}

.mr10 {
  margin-right: 10px;
}
.table-td-thumb {
  display: block;
  margin: auto;
  width: 40px;
  height: 40px;
}

</style>
