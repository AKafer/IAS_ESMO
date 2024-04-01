$(document).ready(function () {
  let table;
  const date_test = $("#date_test");
  const date_input = $("#date_input");

  function create_table(url) {
    console.log("***Table***");
    // const url = "api/?date=2024-03-20";
    console.log(url);
    table = $("#SP_Table").DataTable({
      ajax: {
        url: url,
        dataSrc: "",
      },
      columns: [
        { data: "number"},
        { data: "name" },
        { data: "type_1" },
        { data: "date_type_1" },
        { data: "type_2"},
        { data: "date_type_2"},
        { data: "duration"},
      ],
      DisplayLength: 10,
      processing: true,
      lengthMenu: [
        [20, -1],
        [20, "Все"],
      ],
    });
  }



  $("#TableButton").on("click", function () {
      console.log(date_test.val());
      date_input.val('ЖОПАКАКАЯТО');
      console.log(date_input.val());
      $("#data-input").val($("#data-test").val());
      if (table) {
        const url = "api/?date=2024-03-20";
        table.ajax.url(url).load();
      } else {
        create_table("api/?date=2024-03-20");
      }


  //   const selectedFile = document.querySelector("#input_csv").files[0];
  //   console.log(selectedFile);
  //   console.log($("#input_csv").val());
  //
  //   csrftoken = window.CSRF_TOKEN;
  //   function csrfSafeMethod(method) {
  //     // these HTTP methods do not require CSRF protection
  //     return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  //   }
  //   $.ajaxSetup({
  //     beforeSend: function (xhr, settings) {
  //       if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
  //         xhr.setRequestHeader("X-CSRFToken", csrftoken);
  //       }
  //     },
  //   });
  //
  //   var data = new FormData();
  //   data.append("file", selectedFile);
  //   console.log("datA", data);
  //
  //
  //
  //   $.ajax({
  //     type: "POST",
  //     url: "api/files/",
  //     data: data,
  //     processData: false,
  //     contentType: false,
  //     success: function (data) {
  //       console.log(JSON.stringify(data));
  //       filename = "res.json";
  //       $.ajax({
  //         type: "GET",
  //         url: "/api/files/download_json/",
  //         success: function (response) {
  //           var blob = new Blob([response]);
  //           var link = document.createElement("a");
  //           link.href = window.URL.createObjectURL(blob);
  //           link.download = filename;
  //           link.click();
  //           if (table) {
  //             const url = "/api/players/from_last_file/";
  //             table.ajax.url(url).load();
  //           } else {
  //             create_table();
  //           }
  //         },
  //       });
  //     },
  //     error: function (errMsg) {
  //       alert(`Ошибка при создании файла\n${JSON.stringify(errMsg)}`);
  //       console.log(JSON.stringify(errMsg));
  //     },
  //   });
  });
});