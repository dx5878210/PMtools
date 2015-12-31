$.ajaxSetup({
                 data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
            });
<script src={% static 'jquery/jquery.min.js' %}></script>
    <script>
        $(document).ready(function(){
            $.ajaxSetup({
                 data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
            });
        $('#formadd').submit(function(){
                var name = $("#id_name").val();                 //获得form中用户输入的name 注意这里的id_name 与你html中的id一致
                var password = $("#id_password").val();    //同上
               
                $.ajax({
                    type:"POST",
                    data: {name:name, password:password},
                    url: "{% url 'blog:comments_upload' %}", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
                    cache: false,
                    dataType: "html",
                    success: function(result, statues, xml){
                        alert(result);                                         //成功时弹出view传回来的结果
                    },
                    error: function(){
                        alert("false");
                    }
                });
                return false;
            });

        });
    </script>


