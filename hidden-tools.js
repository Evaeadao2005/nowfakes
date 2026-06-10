(function () {
  "use strict";

  function initGokuForm() {
    var form = document.getElementById("goku-fakes-form");
    if (!form) return;
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var qtd = document.getElementById("qtdFakes").value;
      var servidor = document.getElementById("servidor").value;
      var regiao = document.getElementById("regiao").value;
      var amizade = document.getElementById("amizade").checked ? "Sim" : "Não";
      var raspadinha = document.getElementById("raspadinha").checked ? "Sim" : "Não";
      var mensagem = "Olá! Quero solicitar " + qtd + " fake(s) no servidor " + servidor + ", região " + regiao + ". Serviço de adicionar amizade: " + amizade + ". Deseja mandar raspadinha: " + raspadinha + ".";
      window.open("https://wa.me/5521984295108?text=" + encodeURIComponent(mensagem), "_blank", "noopener,noreferrer");
    });
  }

  var servidores = [
    ["pt", "5"], ["pt", "20"], ["pt", "37"], ["pt", "61"], ["pt", "86"], ["pt", "121"], ["pt", "148"], ["pt", "184"],
    ["pt", "221"], ["pt", "250"], ["pt", "302"], ["pt", "332"], ["pt", "373"], ["pt", "413"], ["pt", "458"], ["pt", "503"],
    ["pt", "548"], ["pt", "593"], ["pt", "638"], ["pt", "653"], ["pt", "668"], ["pt", "683"], ["pt", "688"], ["pt", "693"],
    ["pt", "698"], ["pt", "713"], ["pt", "718"], ["pt", "728"], ["pt", "738"], ["pt", "743"], ["pt", "753"], ["pt", "758"],
    ["pt", "773"], ["pt", "778"], ["pt", "783"], ["pt", "788"], ["pt", "793"], ["pt", "798"], ["pt", "799"], ["pt", "800"],
    ["pt", "801"], ["pt", "802"], ["pt", "803"], ["pt", "804"], ["pt", "805"], ["pt", "806"], ["pt", "807"], ["pt", "808"],
    ["pt", "809"], ["pt", "810"], ["pt", "811"]
  ];

  function generateRandomCode(length) {
    var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    var code = "";
    for (var i = 0; i < length; i += 1) {
      code += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return code;
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).then(function () { return true; }).catch(function () { return false; });
    }
    var textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    var ok = false;
    try {
      ok = document.execCommand("copy");
    } catch (error) {
      ok = false;
    }
    document.body.removeChild(textarea);
    return Promise.resolve(ok);
  }

  function setLink(id, href, label, action) {
    var slot = document.getElementById(id);
    if (!slot) return;
    if (action === "popup") {
      slot.innerHTML = '<button class="tool-button tool-button--orange" type="button" data-open-popup="' + href + '">' + label + "</button>";
    } else {
      slot.innerHTML = '<a href="' + href + '" target="_blank" rel="noopener noreferrer">' + label + "</a>";
    }
  }

  function initDivulgador() {
    var tool = document.getElementById("divulgador-tool");
    if (!tool) return;
    var nicks = {
      nick1: "Kaze´Vex",
      nick2: "S130-Kazu",
      nick3: "S702-KhaLiL",
      nick4: "S773-Neljjz"
    };

    tool.addEventListener("click", function (event) {
      var popup = event.target.closest && event.target.closest("[data-open-popup]");
      if (popup) {
        window.open(popup.getAttribute("data-open-popup"), "_blank", "width=800,height=600,noopener,noreferrer");
        return;
      }

      var button = event.target.closest && event.target.closest("[data-divulgador-action]");
      if (!button) return;
      var action = button.getAttribute("data-divulgador-action");
      if (nicks[action]) {
        copyText(nicks[action]).then(function () {
          var oldText = button.textContent;
          button.textContent = "Nick copiado";
          setTimeout(function () { button.textContent = oldText; }, 1200);
        });
        return;
      }
      if (action === "recall") {
        window.open("https://narutorecall.oasgames.com/pt/return", "_blank", "width=800,height=600,noopener,noreferrer");
        return;
      }
      if (action !== "gerar") return;

      var input = document.getElementById("codigoInput");
      var codigo = input && input.value ? input.value.trim() : generateRandomCode(12);
      var servidor = servidores[Math.floor(Math.random() * servidores.length)];
      var codigoCompleto = codigo + "|" + servidor[1] + "|" + servidor[0];
      copyText(codigoCompleto);
      var registro = "https://passport.narutowebgame.com/index.php?m=register&email=" + encodeURIComponent(codigoCompleto) + "&pwd=080808";
      var login = "https://passport.narutowebgame.com/index.php?m=login&email=" + encodeURIComponent(codigoCompleto) + "&pwd=080808";
      var jogo = "https://naruto.narutowebgame.com/" + servidor[0] + "/serverlist/s" + servidor[1] + "?leftbar_collapse=yes&logintype=4";
      setLink("registroLink", registro, "Abrir cadastro gerado");
      setLink("loginLink", login, "Abrir login gerado");
      setLink("gameLink", jogo, "Abrir servidor " + servidor[1], "popup");
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initGokuForm();
    initDivulgador();
  });
})();
