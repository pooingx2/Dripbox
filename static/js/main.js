$(document).ready(function(){

    $('#loginBtn').click(function(){

        var email = $('#loginEmail').val();
        var pwd = $('#loginPwd').val();

        var reg_email=/^[-A-Za-z0-9_]+[-A-Za-z0-9_.]*[@]{1}[-A-Za-z0-9_]+[-A-Za-z0-9_.]*[.]{1}[A-Za-z]{2,5}$/;

        if(email.search(reg_email) == -1){
            alert("이메일 형식을 확인해주세요");
        }
        else if(pwd.length < 6){
            alert("비밀번호가 짧습니다.");
        }
        else{
            $.ajax({
                type : "POST",
                url : '/login/',
                data :{
                    email: email,
                    pwd: pwd
                },
                dataType: "json",
                success:function(data){
                    console.log(data);
                    alert("msg : " + data['msg']);
                    if(data['status']==1) {
                        $('#loginCloseBtn').click()
                        location.href = "/home/";
                    }
                },
                error : function(xhr, status, error) {
                    alert("Status : " + status + "\n" + "Error : " + error);
                }
            });
        }
    });

    $('#signupBtn').click(function(){
        var email = $('#signupEmail').val();
        var pwd1 = $('#signupPwd1').val();
        var pwd2 = $('#signupPwd2').val();

        var reg_email=/^[-A-Za-z0-9_]+[-A-Za-z0-9_.]*[@]{1}[-A-Za-z0-9_]+[-A-Za-z0-9_.]*[.]{1}[A-Za-z]{2,5}$/;

        if(email.search(reg_email) == -1){
            alert("이메일 형식을 확인해주세요");
        }
        else if(pwd1 != pwd2){
            alert("비밀번호를 확인해주세요");
        }
        else if(pwd1.length < 6 || pwd1.length < 6){
            alert("비밀번호가 짧습니다.");
        }
        else{
            $.ajax({
                type : "POST",
                url : '/signup/',
                data :{
                    email: email,
                    pwd: pwd1
                },
                dataType: "json",
                success:function(data){
                    console.log(data);
                    alert("msg : " + data['msg']);
                    if(data['status']==1) {
                        $('#signupCloseBtn').click()
                    }
                },
                error : function(xhr, status, error) {
                    alert("Status : " + status + "\n" + "Error : " + error);
                }
            });
        }
    });

    $('#loginModalBtn').click(function(){
        $('#loginEmail').val("");
        $('#loginPwd').val("");
    });

    $('#signupModalBtn').click(function(){
        $('#signupEmail').val("");
        $('#signupPwd1').val("");
        $('#signupPwd2').val("");
    });

});