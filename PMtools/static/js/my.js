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
                var name = $("#id_name").val();                 //���form���û������name ע�������id_name ����html�е�idһ��
                var password = $("#id_password").val();    //ͬ��
               
                $.ajax({
                    type:"POST",
                    data: {name:name, password:password},
                    url: "{% url 'blog:comments_upload' %}", //��̨��������url �����õ���static url ��Ҫ��urls.py�е�nameһ��
                    cache: false,
                    dataType: "html",
                    success: function(result, statues, xml){
                        alert(result);                                         //�ɹ�ʱ����view�������Ľ��
                    },
                    error: function(){
                        alert("false");
                    }
                });
                return false;
            });

        });
    </script>


