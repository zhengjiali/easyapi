// import {loading} from "./common.js"
// 解码  
function decodeUnicode(str) {  
    str = str.replace(/\\/g, "%");  
    return unescape(str);  
}
// 查询方法
function case_query(currPage, limit) {
    var currPage = 1;
        $.ajax({
          type : "Get",
          url : "rest_case_list_content/???",
          data : {
            "currPage" : currPage,
            "sortType" : "desc"
            },
          dataType : "json",
          success : function(data) {
            var data_content = data["data"];
            var totalCount = queryTatol();//数据总条数
            // var totalCount = data["count"];//数据总条数
            var showCount = 10;//显示的页数
            var limit = 10;//每页显示的数据条数
            case_createTable(1, limit, totalCount, data_content);
            $("#fenye").extendPagination(
            {
              totalCount : totalCount,
              showCount : showCount,
              limit : limit,
              callback : function(currPage,limit,totalCount) {
                $.ajax({
                  type : "Get",
                  url : "rest_api_list_content/???",
                  // url : "http://172.19.162.104:8000/api/apis",
                  data : {
                    "currPage" : currPage,
                    "sortType" : "desc"
                  },
                  dataType : "json",
                  success : function(data) {
                    var data_content = data["data"];
                    case_createTable(currPage,limit,totalCount,data_content);
                  },
                  error : function(data) {
                    $("#error_mess").html("系统异常！");
                    $("#confirm_error").slideDown();
                  }
                });
              }
            });
          },
          error : function(data) {
             $("#error_mess").html("系统异常！");
             $("#confirm_error").slideDown(); 
          }
        });
  }  
//查询数据总条数
function case_queryTatol() {
    var keywords = $("#keywords").val();
    $.ajax({
      type : "Get",
      url : "rest_api_list_count/??",
      data : {keyword:keywords},
      dataType : "json",
      async : false,
      success : function(data) {
        totalCount = data["count"];
      },
      error : function(data) {
        $("#error_mess").html("系统异常！");
        $("#confirm_error").slideDown(); 
      }
    });
    return totalCount;
  }
// 创建列表
function case_createTable(currPage,limit, totalCount, data) {
    let html = [], showNum = limit;
    console.log(data);
    if (totalCount - (currPage * limit) < 0) {
      showNum = totalCount - ((currPage - 1) * limit);  
    }                          
    html.push('<table class="table table-hover">');
    html.push('<thead><tr><th style="width:150px;">接口类别</th><th style="width:250px;">接口名称</th><th style="width:100px;">接口类型</th><th style="width:330px;">URL</th><th style="width:200px;">更新时间</th><th style="width:220px;">操作</th></tr></thead><tbody>');
    for (let i = 0; i < showNum; i++) {
      if (i < data.length) {
        // html.push('<tr><td id='+data[i].id+'>'+data[i].proj+'</td>');
        // html.push('<td>'+data[i].name+'</td>');
        // html.push('<td>'+data[i].method+'</td>');
        // html.push('<td>'+data[i].path+'</td>');
        // html.push('<td>'+data[i].update_time+'</td>');
        html.push('<tr><td id='+data[i][0]+'>'+data[i][5]+'</td>');
        html.push('<td>'+data[i][1]+'</td>');
        html.push('<td>'+data[i][2]+'</td>');
        html.push('<td>'+data[i][3]+'</td>');
        html.push('<td>'+data[i][4]+'</td>');
        html.push('<td><button type="button" class="btn btn-link " id="account_pwd_reset'+i+'" style="outline:none;width:38px;height:23px; padding:0px;" onClick="apiEdit(this)">编辑</button><button type="button" class="btn btn-link process_delete" id="delete_account'+i+'" style="outline:none;width:38px;height:23px; padding:0px;" onClick="apiDelete(this)">删除</button><button type="button" class="btn btn-link process_delete" id="delete_account'+i+'" style="outline:none;width:65px;height:23px; padding:0px;" onClick="apiTestCase(this)">用例管理</button></td>');
        html.push('</tr>');
      }
    }
    html.push('</tbody></table>');
    let mainObj = $('#center_content_table');
    mainObj.empty();
    mainObj.html(html.join(''));
    loading(1);
  };
//跳转新增界面
function apiAdd(){
  window.location.href = "/Voldemort/api_add";
}
//跳转编辑界面
function apiEdit(id){
  let api_id = $(id).parent().parent().children().eq(0).attr("id");
  window.location.href = "/Voldemort/api_edit?id="+api_id;
}
  //进入用例管理界面方法
function apiTestCase(id){
    let api_id = $(id).parent().parent().children().eq(0).attr("id");
    window.location.href = "/Voldemort/api_TestCase?id="+api_id;
}