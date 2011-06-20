function filtraNutriente(texto){
    var texto = $(texto).val();
    $("#resultado").html("");
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/filtrarIngrediente/",
        dataType: "json",
        data : {
                'texto' : texto
        },
        success: function(retorno){
            $("#resultado").html("");
            linhas = "";
            $.each(retorno, function(key, obj){
                linhas = linhas + "<tr>\
                                    <td align=center>\
                                        <input type=\"button\" onclick=\"javascript:adicionarIngrediente(" + obj.pk + ");\" name=\"adicionar\" value=\"Adicionar a Receita\" id=\""+ obj.pk +"\">\
                                        &nbsp;<br>\
                                        Quantidade: <input type=\"text\" size=\"4\" value=\"0\" name=\"qtd"+obj.pk+"\" id=\"qtd"+obj.pk+"\">\
                                    </td>\
                                    <td>"+obj.fields.nome+"\
                                    </td>\
                                    <td>\
                                        <span id=\""+ obj.pk + "\" onmouseup=\"javascript:mostrarNutrientes(this)\">\
                                            Mostrar("+obj.fields.nutriente+")\
                                        </span>\
                                        <div id=\"nutrientes_"+obj.pk+"\">\
                                        </div>\
                                    </td>\
                                   </tr>";
            });
            $("#resultado").append("<table width=100% id=teste><tr><td width=30% align=center>Op&ccedil;&otilde;es</td><td width=50%>Ingrediente</td><td>Nutrientes</td></tr>" + linhas + "</table>");
        }
    });
}

function mostrarNutrientes(valor){
    var ingrediente = $(valor).attr("id");
    $("#nutrientes").html("");
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/mostrarNutrientes/",
        dataType: "json",
        data : {
                'ingrediente' : ingrediente
        },
        success: function(retorno){
            $("#nutrientes_"+ingrediente).html("");
            $.each(retorno, function(key, obj){
                    $("#nutrientes_"+ingrediente).append(obj.fields.nome+"<br>");
            }); 
        }
    });
}
function adicionarIngrediente(valor){
    var idIngrediente = valor;
    var quantidade = $("#qtd"+valor).val();
    var idreceita = 0;
    var tipo = $("#tipo").val();
    var nomereceita = $("#nome").val();
    if ($("#idreceita").val()){
        idreceita = $("#idreceita").val();
    }
    alert("idIngrediente: "+idIngrediente+ " - quantidade: "+quantidade+" idreceita: "+idreceita);
    $("#receita").html("");
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/adicionarIngrediente/",
        dataType: "json",
        data : {
                'ingrediente' : idIngrediente,
                'quantidade'  : quantidade,
                'idReceita'   : idreceita,
                'tipo'        : tipo,
                'nomereceita' : nomereceita
        },
        success: function(retorno){
            $("#receita").html("");
            linha = "";
            keys = getKeys(retorno);
            keys = keys.reverse();
            total = keys.length;
            
            for (i=0; i<total; i++){
                    $("#receita").append("<div id=\""+ obj.pk +"\"> [X] "+ obj.fields.nome + " - (" + obj.fields.quantidade + ")</div><hr>");
            }
            
        }
    });
}


function getKeys(obj) {
    keys = new Array();
    for (key in obj) {
        keys.push(key);
    }
    return keys;
}