<template>
  <div class="container">
    <div class="content-title">模型本地上传</div>
    <div class="plugins-tips">
      <!--      <a href="https://element-plus.org/zh-CN/component/upload.html" target="_blank">Element Plus Upload</a>-->
      <p style="line-height: 30px">
        建议上传的文件格式为ultralytics可兼容的，文件名中途是不可修改的，除非删除再上传一次
      </p>

      <p style="line-height: 30px">
        首先先上传对应的pt文件,然后进行缓存,最后将填写的信息提交到终端
      </p>

      <p style="line-height: 30px">
        如果重复提交多次到缓存里,则最新的一次会覆盖掉之前的
      </p>

      <p style="line-height: 30px">
        注意填写模型名称的时候不要于现有的模型名称重复
      </p>
    </div>
    <div class="form-box">

      <el-form ref="formRef" :model="AddModelForm" label-width="80px" :rules="rules">
        <el-form-item label="模型名称" prop="model_name" label-width="150px">
          <el-input v-model="AddModelForm.model_name"></el-input>
        </el-form-item>

        <el-form-item label="模型种类" prop="model_type" label-width="150px">
          <el-select v-model="AddModelForm.model_type" placeholder="请选择">
            <el-option key="yolov5" label="yolov5" value="yolov5"></el-option>
            <el-option key="yolov8" label="yolov8" value="yolov8"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="对应数据集名称" prop="model_dataset" label-width="150px">
          <el-input v-model="AddModelForm.model_dataset"></el-input>
        </el-form-item>


        <el-form-item label="上传文件" label-width="150px">
          <el-upload
              class="upload-demo"
              drag
              :limit="1"
              :show-file-list="true"
              action="http://localhost:5000/upload/model/"
              multiple
              :on-success="handleUploadCache"
          >
            <!--   action是将图片file文件直接上传到后端服务器上，要想将图片附带的数据信息上传必须要实现额外函数 -->
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或
              <em>点击上传</em>
            </div>
          </el-upload>
        </el-form-item>

        <el-form-item label-width="150px" label="操作">
          <el-button type="primary" @click="handleModelPost(AddModelForm)">表单提交</el-button>
          <el-button type="warning" @click="handleModelFormReset">重置表单</el-button>
        </el-form-item>

      </el-form>
    </div>

    <div>
      <div class="content-title">当前模型</div>

      <el-descriptions :column="3" border title="检测模型">
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

    </div>

    <div>
      <div class="content-title">模型管理</div>
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


        <el-table-column label="操作" width="300" align="center">
          <template #default="scope">
<!--            <el-button text :icon="Search" class="green" @click="handleModelDetail(scope.$index, scope.row)" v-permiss="15">-->
<!--              查看-->
<!--            </el-button>-->
            <el-button text :icon="TopLeft" class="primary" @click="handleModelChoose(scope.$index, scope.row)" v-permiss="15">
              选中
            </el-button>
            <el-button text :icon="Edit" @click="handleModelEdit(scope.$index, scope.row)" v-permiss="15">
              编辑
            </el-button>
            <el-button text :icon="Delete" class="red" @click="handleModelDelete(scope.row)" v-permiss="16">
              删除
            </el-button>
          </template>
        </el-table-column>
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


      <div class="content-title">图片检测</div>

      <div class="plugins-tips">
        <!--      <a href="https://element-plus.org/zh-CN/component/upload.html" target="_blank">Element Plus Upload</a>-->
        <p style="line-height: 20px">
          点击检测即可得到该图片在当前模型的检测结果，但需要等待几秒钟
        </p>
      </div>

      <div class="handle-box">
        <el-input v-model="query.keyword" placeholder="文件名称" class="handle-input mr10"></el-input>
        <el-button type="primary" :icon="Search " @click="handleSearch">搜索</el-button>

<!--        <el-button type="primary"  @click="getData">-->
<!--          <el-icon><Refresh /></el-icon>-->
<!--          <span>刷新页面</span>-->
<!--        </el-button>-->

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

        <!--      <el-table-column prop="date" label="注册时间"></el-table-column>-->
        <el-table-column label="操作" width="220" align="center">
          <template #default="scope">
            <el-button text :icon="Search" class="green" @click="detection(scope.$index, scope.row)" v-permiss="16">
              检测
            </el-button>
          </template>
        </el-table-column>
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

      <el-dialog title="编辑" v-model="editVisible" width="30%">
        <el-form label-width="100px">
<!--          <el-form-item label="用户名">-->
<!--            <el-input v-model="form.name"></el-input>-->
<!--          </el-form-item>-->
<!--          <el-form-item label="地址">-->
<!--            <el-input v-model="form.address"></el-input>-->
<!--          </el-form-item>-->
          <el-form-item label="模型ID">
            <span>{{form.wid}}</span>
          </el-form-item>

          <el-form-item label="文件名">
            <span>{{form.mdoel_name}}</span>
          </el-form-item>

          <el-form-item label="模型种类" prop="region">
            <el-select v-model="form.model_type" placeholder="请选择">
              <el-option key="yolov5" label="yolov5" value="yolov5"></el-option>
              <el-option key="yolov8" label="yolov8" value="yolov8"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="对应数据集">
            <el-input v-model="form.model_dataset"></el-input>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="editVisible = false">取 消</el-button>
            <el-button type="primary" @click="saveModelEdit">确 定</el-button>
          </span>
        </template>
      </el-dialog>


      <el-dialog title="模型细节" v-model="detailVisible" width="30%">
      <el-form label-width="100px">
        <!--          <el-form-item label="用户名">-->
        <!--            <el-input v-model="form.name"></el-input>-->
        <!--          </el-form-item>-->
        <!--          <el-form-item label="地址">-->
        <!--            <el-input v-model="form.address"></el-input>-->
        <!--          </el-form-item>-->


      </el-form>
      <template #footer>
          <span class="dialog-footer">
            <el-button @click="detailVisible = false" >退出</el-button>
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

interface TableItem { // 定义图片的接口

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

// 下面定义的是file表相关的数据
const query = reactive({
  curPage: 1,
  pageSize: 10,
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

// 下面是定义当前后端使用那个model的表相关数据信息
const model_params = reactive({
  "model_dataset": "null",
  "model_name": "null",
  "model_type": "null",
  "wid": -1
})

const getCurModel = () => { // 获取后端当前使用的模型信息
  axios({
    method: 'GET',
    url: '/current',
  }).then(res=>{
    // console.log(res)
    model_params.model_dataset =  res.data.results.model_dataset
    model_params.model_name = res.data.results.model_name
    model_params.model_type = res.data.results.model_type
    model_params.wid = res.data.results.wid
    // console.log(model_params)
  })
}

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


onMounted(() => {
  getData()
  getModelData()
  getCurModel()
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

const handleUploadCache = (response: any) =>{
  if(response.status == 'success'){
    ElMessage.success('上传暂缓PT文件成功')
  }
  else{
    ElMessage.error('上传暂缓文件PT文件失败')
  }
}

/***
 模型相关操作
 ***/

//模型表格编辑时弹窗和保存
const editVisible = ref(false);
let form = reactive({
  wid: -1,
  mdoel_name: '',
  model_type: 'yolov8',
  model_dataset: '',
});

let idx: number = -1;
const handleModelEdit = (index: number, row: any) => {
  idx = index;
  form.model_type = row.model_type;
  form.model_dataset = row.model_dataset
  form.mdoel_name = row.model_name
  form.wid = row.wid;
  editVisible.value = true;
};

const saveModelEdit = () => {
  axios({
    method: 'PUT',
    url: '/wmodel/' + form.wid,
    data: {
      'model_name': form.mdoel_name,
      'model_type': form.model_type,
      'model_dataset': form.model_dataset
    },
  }).then(res=>{
    if(res.data.status == 'success'){
      editVisible.value = false
      alert("模型信息修改成功")
      getModelData()
    }
    // console.log(tableData)
  })
}

const handleModelChoose = (index: number, row: any) => {
    axios(
        {
          method: 'PUT',
          url: '/switch',
          data: row
        }
    ).then(res=>{
      if(res.data.status == 'success'){
        ElMessage.success('切换模型成功');
        getCurModel()
      }
    })
}

//上传添加新模型相关操作
const AddModelForm = reactive({
  model_name: '',
  model_type: 'yolov8',
  model_dataset: ''
})

// 查看模型的内部细节
const detailVisible = ref(false)

const handleModelDetail = (index: number, row: any) =>{
  detailVisible.value = true
  // console.log(row)
  axios({
    method: 'GET',
    url: '/detail/model',
    params: row
  }).then(res => {
    console.log(res)
    if(res.data.status == 'success'){

    }
  })
}

// 上传模型相关信息

const handleModelPost = (form: any) => {
  // console.log("114514")
  // console.log(form)
  if(form.model_dataset.length == 0 || form.model_name.length < 3){
    ElMessage.error('提交失败,请检查是否符合表格要求')
  }
  else{
    axios({
      method: 'POST',
      url: '/wmodel', // 这里的后端请求url功能和文件复制是耦合的，也就是 复制pt -> 创建pt信息
      data: {
        'model_name': form.model_name,
        'model_dataset': form.model_dataset,
        'model_type': form.model_type
      }
    }).then(res => {
      if(res.data.status == 'success'){
        ElMessage.success('模型上传成功')
        getModelData()
      }
      else{
        ElMessage.error('模型上传失败')
      }
    })
  }
}

const handleModelFormReset = () => {
  AddModelForm.model_name = ''
  AddModelForm.model_type = 'yolov8'
  AddModelForm.model_dataset = ''
}

const rules = reactive<FormRules>({
  model_name: [
    {required: true, message: '请输入模型名称', trigger: 'blur' },
    {min: 3, message: '长度至少为3', trigger: 'blur'}
  ],
  model_dataset:[
    { required: true, message: '请输入数据集名称', trigger: 'blur' },
  ]
})

// 删除操作
const handleModelDelete = (scope: any) => {
  // console.log(scope)
  if(scope.wid <= 6){
    ElMessage.error('系统不允许删除前六个固定模型')
  }
  else{

    if(scope.wid != model_params.wid){
      ElMessageBox.confirm('确定要删除吗？', '提示', {
        type: 'warning'
      }).then(()=>{
        axios({
          method: 'delete',
          url: '/wmodel/' + scope.wid  // 这里的后端请求url功能和文件删除是耦合的，也就是 删除pt -> 删除pt信息
        }).then(res => {
          if(res.data.status == 'success'){
            ElMessage.success('删除模型成功')
            getModelData()
          }else{
            ElMessage.error('删除模型失败')
          }
        })
      })
    }
    else{
      ElMessage.error('删除的模型是当前后端所使用的模型')
    }
  }
}


/**
 * 实现图片检测相关操作
 */
const detection = (index: number, row: any) => {
  console.log(row)
  axios({ // 首先执行检测任务，生成结果图片
    method: 'POST',
    url: '/detect',
    data: row
  }).then(res1=>{
    // console.log(res1)
    if(res1.data.status == 'success'){ // 然后再把result得到的json传入到数据库中
      axios({
        method: 'POST',
        url: '/result',
        data: res1.data.results.log
      }).then(res2=>{
        // console.log(res2)
        if(res2.data.status == 'success'){ // 最后再把obj信息传入到obj中
          axios({
            method: 'POST',
            url: '/obj',
            data: res1.data // 在/detect后端哪里得到的json信息
          }).then(res3 => {
            // console.log(res3)
              if(res3.data.status == 'success'){
                ElMessage.success('目标图片检测成功，保存的文件名称是:\n'
                    + res1.data.results.log.filename + '_' +
                    res1.data.results.log.timestamp + '.' + res1.data.results.log.type);
              }
          })
        }
      })
    }
    else{
      ElMessage.error('检测中途出现异常')
    }
  })
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

.my-label {
  background: var(--el-color-success-light-9);
}
.my-content {
  background: var(--el-color-danger-light-9);
}

</style>
