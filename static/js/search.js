$("#search").click(
    function ()
    {
        if ($("#keyword").val()==="")
        {
            window.location.pathname = "search";
        }
        else
        {
            window.location.pathname = "search&keyword="+$("#keyword").val();
        }
    }
)
function callback(data,status)
{
    let dat = JSON.parse(data);
    let msg="";
    if (dat["len"]===0)
        msg = "ѡ�β����ɹ�";
    else
    {
        msg = dat["len"]+"���γ�ѡ��ʧ�ܣ�ʧ�ܵĿγ̺����¡�\n";
        for (let i=0;i<dat["list"].length;i++)
        {
            msg+=(dat['list'][i]+"\n");
        }
        msg+="��ȷ����֮ǰ��δѡ����Щ�γ̡�";
    }
    alert(msg);
}
$("#select").click(
    function ()
    {
        let list = [];
        let $_check = $(".check");
        let $_course = $(".course");
        for (let i=0;i<$_check.length;i++)
        {
            if ($_check.get(i).checked)
            {
                list.push($_course.get(4*i).innerHTML);
            }
        }
        if (list.length===0)
            return;
        let csrf = $("#csrf").val();
        $.post("", {"content":list, "csrfmiddlewaretoken":csrf},
            callback);
    }
)