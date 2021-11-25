$(document).ready(function(){
})

function add_moto(){


	var tableRef = document.getElementById('tabela_moto').getElementsByTagName('tbody')[0];
	var table = document.getElementById("tabela_moto");
	var row = table.insertRow(tableRef.rows.length);
	var cell1 = row.insertCell(0);
	var cell2 = row.insertCell(1);
	cell1.innerHTML = tableRef.rows.length-1;
	cell2.innerHTML = $('#motorista').val();

}