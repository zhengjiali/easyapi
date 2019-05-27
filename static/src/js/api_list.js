// 解码
function decodeUnicode(str) {  
    str = str.replace(/\\/g, "%");  
    return unescape(str);  
}
// 查询方法
function query(currPage, limit) {
    var currPage = 1;
    var keywords = $("#keywords").val();
    var project = $("#keytypes option:selected").attr("value");
    console.log(project);
        $.ajax({
          type : "Get",
          url : "/api/apis",
          data : {
            "currPage" : currPage,
            "kw" : keywords,
            "sortType" : "desc",
            "project" : project
            },
          dataType : "json",
          success : function(data) {
            var data_content = data["data"];
            var totalCount = data["count"];//数据总条数
            console.log(totalCount);
            var showCount = 10;//显示的页数
            var limit = 10;//每页显示的数据条数
            createTable(1, limit, totalCount, data_content);
            $("#fenye").extendPagination(
            {
              totalCount : totalCount,
              showCount : showCount,
              limit : limit,
              callback : function(currPage,limit,totalCount) {
                $.ajax({
                  type : "Get",
                  url : "/api/apis",
                  data : {
                    "currPage" : currPage,
                    "kw" : keywords,
                    "sortType" : "desc",
                    "project" : project
                  },
                  dataType : "json",
                  success : function(data) {
                    var data_content = data["data"];
                    createTable(currPage,limit,totalCount,data_content);
                  },
                  error : function(data) {
                    pop_error("系统异常！");
                  }
                });
              }
            });
          },
          error : function(data) {
           pop_error("系统异常！");
          }
        });
  }  
// 创建列表
function createTable(currPage,limit, totalCount, data) {
    let html = [], showNum = limit;
    if (totalCount - (currPage * limit) < 0) {
      showNum = totalCount - ((currPage - 1) * limit);  
    }
    if (data.length >= 1) {                        
    html.push('<table class="table table-hover">');
    html.push('<thead><tr><th style="width:150px;">所属项目</th><th style="width:250px;">接口名称</th><th style="width:100px;">接口类型</th><th style="width:330px;">URL</th><th style="width:200px;">更新时间</th><th style="width:220px;">操作</th></tr></thead><tbody>');
    for (let i = 0; i < showNum; i++) {
      if (i < data.length) {
        html.push('<tr><td id='+data[i].id+'>'+data[i].proj+'</td>');
        html.push('<td>'+data[i].name+'</td>');
        html.push('<td>'+data[i].method+'</td>');
        html.push('<td>'+data[i].path+'</td>');
        html.push('<td>'+data[i].update_time+'</td>');
        html.push('<td><button type="button" class="btn btn-link table_btn_lef" onClick="apiEdit(this)">编辑</button><button type="button" class="btn btn-link table_btn_lef" onClick="apiDelete(this)">删除</button><button type="button" class="btn btn-link table_btn_mid" onClick="apiTestCase(this)">用例管理</button></td>');
        html.push('</tr>');
      }
    }
    html.push('</tbody></table>');
    let mainObj = $('#center_content_table');
    mainObj.empty();
    mainObj.html(html.join(''));
  }
  else{
    nodata_img("center_content_table",1);
  }
  loading(1);
};
//跳转新增界面
function apiAdd(){
      window.location.href = "/api/addApi/";
}
//跳转编辑界面
function apiEdit(id){
    let api_id = $(id).parent().parent().children().eq(0).attr("id");
      window.location.href = "/api/"+api_id+"/edit/";
}
//跳转用例管理界面
function apiTestCase(id){
    let api_id = $(id).parent().parent().children().eq(0).attr("id");
      window.location.href = "/api/"+api_id+"/cases/";
}

//初始化fileinput控件（第一次初始化）
function initFileInput(ctrlName, uploadUrl) {    
  var control = $('#' + ctrlName); 

  control.fileinput({
      language: 'zh', //设置语言
      uploadUrl: uploadUrl, //上传的地址
      allowedFileExtensions : ['jpg', 'png','gif'],//接收的文件后缀
      showUpload: false, //是否显示上传按钮
      showCaption: false,//是否显示标题
      browseClass: "btn btn-primary", //按钮样式             
      previewFileIcon: "<i class='glyphicon glyphicon-king'></i>", 
  });
}

// 导入用例
function upload(){
  var fileObj = document.getElementById("file").files[0];
  var formData = new FormData();
  formData.append('myfile',fileObj);
  $.ajax({
    type:"POST",
    url:"/uploadFile",
    data:formData,
    contentType: false,
    processData: false,
    success:function (data) {
      var msg = data["msg"];
      alert(msg);
    }
  });
}