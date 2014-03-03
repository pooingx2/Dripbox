$(document).ready(function(){

//    alert(window.location.pathname);

    function getURLParameter(name) {
        return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null
    }

    var current = getURLParameter('id');
    if(current == null) current = "root"
    var folderID = null;
    var fileID = null;

    $('#downloadBtn').hide(false);
    $('#deleteBtn').hide();

    $('.table .folder').click(function() {
        folderID = $(this).find('td:eq(0)').html();
        fileID = null;
        $('.table tr.selected').removeClass('selected');
        $(this).addClass('selected');
        $('#downloadBtn').hide(false);
        $('#deleteBtn').hide();
    });

    $('.table .file').click(function() {
        fileID = $(this).find('td:eq(0)').html();
        folderID = null;
        $('.table tr.selected').removeClass('selected');
        $(this).addClass('selected');
        $('#downloadBtn').show();
        $('#deleteBtn').show();
    });

    $('#createBtn').click(function() {
        var folderName = $('#folderName').val();

        if(folderName == null || folderName ==""){
            alert("폴더 이름을 입력하세요.");
        }
        else{
            var path = $('#filePath').text();
            $.ajax({
                type : "POST",
                url : '/home/',
                data :{
                    option: "create",
                    name: folderName,
                    type: "folder",
                    size: "--",
                    parent: current,
                    path: path
                },
                dataType: "json",
                success:function(data){
                    console.log(data);
                    alert("msg : " + data['msg']);
                    if(data['status']==1) {
                        $('#loginCloseBtn').click();
                        location.href = location.href;
                    }
                },
                error : function(xhr, status, error) {
                    alert("Status : " + status + "\n" + "Error : " + error);
                }
            });
        }
    });

    $('#uploadBtn').click(function() {
        var fileChooser = document.getElementById("fileChooser");
        var path = $('#filePath').text();

        if(fileChooser.files.length == 0){
            alert("파일을 선택하세요.");
        }
        else{
            var count =0;
            for(var i=0; i<fileChooser.files.length;i++ ){
                var file = fileChooser.files[i];
                if (file) {
                    var dCount = 0;
                    var size = file.size;
                    while(size > 1024 && dCount<4){
                        size = size / 1024;
                        dCount++;
                    }
                    switch(dCount){
                        case 0 : size = size+" Byte"; break;
                        case 1 : size = size+" KB"; break;
                        case 2 : size = size+" MB"; break;
                        case 3 : size = size+" GB"; break;
                        case 4 : size = size+" TB"; break;
                    }

                    var data = new FormData();
                    data.append('option', "upload");
                    data.append('name', file.name);
                    data.append('type', file.type);
                    data.append('size', size);
                    data.append('parent', current);
                    data.append('file', file);
                    data.append('path', path);

                    $.ajax({
                        type : "POST",
                        url : '/home/',
                        data: data,
                        cache: false,
                        contentType: false,
                        processData: false,
                        success:function(data){
                            console.log(data);
                            alert("msg : " + data['msg']);
                            if(data['status']==1 && count == fileChooser.files.length) {
                                $('#uploadCloseBtn').click();
                                location.href = location.href;
                            }
                            count++;
                        },
                        error : function(xhr, status, error) {
                            alert("Status : " + status + "\n" + "Error : " + error);
                            count++;
                        }
                    });
                }
            }
        }
    });

    $('#downloadBtn').click(function() {

        if(folderID == "" && fileID == ""){
            alert("다운로드할 파일을 선택해주세요");
        }
        else if(folderID == null && fileID == null){
            alert("다운로드할 파일을 선택해주세요");
        }
        else{
            var id;
            if(folderID !=null) {
                id=folderID;
            }
            else id=fileID;
            $.ajax({
                type : "POST",
                url : '/home/',
                data :{
                    option: "download",
                    id: id
                },
                dataType: "json",
                success:function(data){
                    console.log(data);
                    alert("msg : " + data['msg']);
                    get_file(data['fileBuf'], data['fileName']);
                },
                error : function(xhr, status, error) {
                    alert("Status : " + status + "\n" + "Error : " + error);
                }
            });
        }
    });

    $('#deleteBtn').click(function() {
           if(folderID == "" && fileID == ""){
            alert("삭제할 파일을 선택해주세요");
        }
        else if(folderID == null && fileID == null){
            alert("삭제할 파일을 선택해주세요");
        }
        else{
            var id;
            if(folderID !=null) {
                id=folderID;
            }
            else id=fileID;
            $.ajax({
                type : "POST",
                url : '/home/',
                data :{
                    option: "delete",
                    id: id
                },
                dataType: "json",
                success:function(data){
                    console.log(data);
                    alert("msg : " + data['msg']);
                    if(data['status']==1) {
                        location.href = location.href;
                    }
                },
                error : function(xhr, status, error) {
                    alert("Status : " + status + "\n" + "Error : " + error);
                }
            });
        }
    });


    $('#createModalBtn').click(function(){
        $('#folderName').val("");
    });

    $('#uploadModal').click(function(){
        $('#fileChooser').val("");
        $('#selectedFile tr:not(:first)').remove();
    });

    var fileChooser = document.getElementById("fileChooser"),
        selectedFile = document.getElementById("selectedFile");

    function traverseFiles (files) {
        var tr, file, fileInfo;

        for (var i=0, il=files.length; i<il; i++) {
            tr = document.createElement("tr");
            file = files[i];
            fileInfo = "<td class=\"name\">"+file.name+"</td>";
//            fileInfo += "<td class=\"type\">"+file.type+"</td>";
            fileInfo += "<td class=\"size\">"+file.size+" Byte</td>";
            tr.innerHTML = fileInfo;
            selectedFile.appendChild(tr);
        };
    };

    fileChooser.onchange = function () {
        traverseFiles(this.files);
    };

    function get_file(buf, filename){

        var uintBuf        = new Uint8Array(buf);
		var textFileAsBlob = new Blob([uintBuf], { type : 'text/plain' });

		var fileNameToSaveAs = filename;

		var downloadLink = document.createElement("a");
		downloadLink.download = fileNameToSaveAs;
		downloadLink.innerHTML = "Download File";
		if (window.webkitURL != null) {
			downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
		} else {
			downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
			downloadLink.onclick = destroyClickedElement;
			downloadLink.style.display = "none";
			document.body.appendChild(downloadLink);
		}
		downloadLink.click();
	}
});