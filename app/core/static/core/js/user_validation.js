document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");

  if (!form) return;

  form.addEventListener("submit", function (event) {
    let valid = true;
    let messages = [];

    // Validação do nome
    const nome = document.getElementById("nome");
    if (!nome.value.trim()) {
      valid = false;
      messages.push("O nome é obrigatório.");
      nome.classList.add("is-invalid");
    } else {
      nome.classList.remove("is-invalid");
    }

    // Validação do e-mail
    const email = document.getElementById("email");
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.value.trim() || !emailRegex.test(email.value)) {
      valid = false;
      messages.push("Informe um e-mail válido.");
      email.classList.add("is-invalid");
    } else {
      email.classList.remove("is-invalid");
    }

    // Validação do perfil
    const perfil = document.getElementById("perfil_id");
    if (!perfil.value) {
      valid = false;
      messages.push("Selecione um perfil.");
      perfil.classList.add("is-invalid");
    } else {
      perfil.classList.remove("is-invalid");
    }

    // Validação da senha (apenas se campo existir - criação)
    const senha = document.getElementById("senha");
    if (senha) {
      if (senha.value.length < 6) {
        valid = false;
        messages.push("A senha deve ter pelo menos 6 caracteres.");
        senha.classList.add("is-invalid");
      } else {
        senha.classList.remove("is-invalid");
      }
    }

    // Impede envio e exibe erros
    if (!valid) {
      event.preventDefault();
      alert(messages.join("\n"));
    }
  });
});
