//请求统计方案结果
function count() {
    var planId = $("#plan_id").val();
    var searchtime = $("#searchTime").val();
    $.ajax({
        type:'Post',
        url:'/statistics/',
        data:{
            "planId":planId,
            "time":searchtime
        },
        dataType:"json",
        success:function(data){
            console.log(data["data"]);
            let msg = data["data"]
            show_result(msg);
            $pre = $("pre");
            $pre.style.maxHeight="1000px";
        },
        error:function (data) {

        }
    });
}

function show_result(data) {
      let html = [];
      let r = data;
      html.push('<div id="result">');
      html.push('<pre>'+syntaxHighlight(r)+'</pre></div>');
      let mainObj = $('.main_content');
        mainObj.empty();
        mainObj.html(html.join(''));
        loading2(1);

}

//格式化json
function syntaxHighlight(json) {
  if (typeof json != 'string') {
    json = JSON.stringify(json, undefined, 2);
  }
  json = json.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>');
  return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function(match) {
    var cls = 'number';
    if (/^"/.test(match)) {
      if (/:$/.test(match)) {
        cls = 'key';
      } else {
        cls = 'string';
      }
    } else if (/true|false/.test(match)) {
      cls = 'boolean';
    } else if (/null/.test(match)) {
      cls = 'null';
    }
    return '<span class="' + cls + '">' + match + '</span>';
  });
}