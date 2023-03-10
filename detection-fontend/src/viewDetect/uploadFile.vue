<template>
  <div class="container">

    <div>
      <div class="content-title">文件本地上传</div>
      <div class="plugins-tips">
        <!--      <a href="https://element-plus.org/zh-CN/component/upload.html" target="_blank">Element Plus Upload</a>-->
        <p style="line-height: 20px">
          建议上传的图片格式为JPG & PNG
        </p>
      </div>

      <el-upload
          class="upload-demo"
          drag
          :limit="1"
          :show-file-list="true"
          action="http://localhost:5000/upload/pic/"
          multiple
          :on-success="upload"
      >
        <!--   action是将图片file文件直接上传到后端服务器上，要想将图片附带的数据信息上传必须要实现额外函数 -->
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          将文件拖到此处，或
          <em>点击上传</em>
        </div>
      </el-upload>
    </div>


    <div>
      <div class="content-title">URL地址上传</div>

      <div class="plugins-tips">
        <!--      <a href="https://element-plus.org/zh-CN/component/upload.html" target="_blank">Element Plus Upload</a>-->
        <p style="line-height: 30px">
          参照的格式如下:
        </p>
        <p style="line-height: 30px">
          https://n.sinaimg.cn/sinakd20220516s/290/w1080h810/20220516/8114-e6ab336af96e393f3f312a58349114d8.png
        </p>
      </div>

      <el-input v-model="url" placeholder="图片url地址" class="handle-input mr10"></el-input>

      <el-button type="primary"  @click="uploadURL(url)">
        <el-icon><Upload /></el-icon>
        <span>上传</span>
      </el-button>
    </div>

    <div class="content-title">图片查询</div>
    <div class="handle-box">
      <el-input v-model="query.keyword" placeholder="文件名称" class="handle-input mr10"></el-input>
      <el-button type="primary" :icon="Search " @click="handleSearch">搜索</el-button>

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
          <el-button text :icon="Delete" class="red" @click="handleDelete(scope.$index)" v-permiss="16">
            删除
          </el-button>
<!--          <el-button text @click="deletePrepare">Click to open the Message Box</el-button>-->
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          v-model:current-page="query.curPage"
          v-model:page-size="query.pageSize"

          :page-sizes="[5, 10, 20]"
          :total="pageTotal"
          @current-change="handlePageChange"
          @size-change="handleSizeChange"

      ></el-pagination>
    </div>

  </div>
</template>

<script lang="ts" setup>
import {ref, reactive, onMounted} from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Delete, Edit, Search, Plus } from '@element-plus/icons-vue';
import axios from "axios";
import {compileScript} from "@vue/compiler-sfc";
// import { fetchData } from '../api/index';

interface TableItem {

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

const query = reactive({
  curPage: 1,
  pageSize: 10,
  tableName: "file",
  keyword: ""
});

const tableData = ref<TableItem[]>([]);  // 表格数据

const pageTotal = ref(0);

const url = ref("")
// 获取表格数据
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


onMounted(() => {
  getData()
  // getNum()
})

// 查询操作
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

// 删除操作
const deletePrepare = (index: number) => {

}
const handleDelete = (index: number) => {
  // 二次确认删除
  ElMessageBox.confirm('确定要删除吗？', '提示', {
    type: 'warning'
  })
      .then(() => {
        var _cache: any = tableData.value[index].fid
        // console.log(tableData.value[index])
        axios.delete("/delete/file", {
          data:{
            type: tableData.value[index].type,
            name: tableData.value[index].name
          }
        }).then(
            res=>{
              // console.log(res.data.status)
              if(res.data.status == 'success'){
                // console.log("1919")
                axios.delete("/files/"+ _cache).then(
                    res2=>{
                      // console.log(res2)
                      if(res2.data.status == 'success'){
                        ElMessage.success('删除成功');
                        tableData.value.splice(index, 1);
                        // alert("删除图片成功")
                        getData()
                      }
                    }
                )
              }
            }
        )
      }
      ).catch(() => {ElMessage.success('删除图片过程中断');});
  // getData()
};

// 本地文件上传相关操作
const upload = (response: any, file: any, filelist: any) => {
  // console.log('114514')
  // console.log(response)
  // console.log("114514")
  // console.log({
  //   width: response.results.width,
  //   height: response.results.height,
  //   origin: response.results.origin,
  //   type: response.results.type,
  //   name: response.results.name,
  // })
    axios.post(
        '/files', {
          width: response.results.width,
          height: response.results.height,
          origin: response.results.origin,
          type: response.results.type,
          name: response.results.name,
        }
    ).then(res=>{
      if(res.data.status == 'success'){
        // console.log(1919810)
        getData()
      }
    })
};


// URL图片上传相关操作
const uploadURL = (url: any) => {
  // console.log(url)
  // console.log("114514")
  axios.post('/upload/url', {
    url: url
  }).then((res)=>{
    if(res.data.status == 'success'){
      axios.post('/files', res.data.results).then(
          (res) => {
            if(res.data.status == 'success'){
              alert('url添加数据成功')
              getData()
            }
            else{
              alert('出现异常')
            }
          }
      )
    }
    else{
      alert("爬取图片失败")
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
  color: #F56C6C;
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
