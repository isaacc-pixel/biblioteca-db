CREATE DATABASE db_trabalho3B;
USE db_trabalho3B;

CREATE TABLE Autores (
    ID_autor INT AUTO_INCREMENT PRIMARY KEY,
    Nome_autor VARCHAR(255) NOT NULL,
    Nacionalidade VARCHAR(255),
    Data_nascimento DATE,
    Biografia TEXT
);

CREATE TABLE Generos (
    ID_genero INT AUTO_INCREMENT PRIMARY KEY,
    Nome_genero VARCHAR(255) NOT NULL
);

CREATE TABLE Editoras (
    ID_editora INT AUTO_INCREMENT PRIMARY KEY,
    Nome_editora VARCHAR(255) NOT NULL,
    Endereco_editora TEXT
);

CREATE TABLE Livros (
    ID_livro INT AUTO_INCREMENT PRIMARY KEY,
    Titulo VARCHAR(255) NOT NULL,
    Autor_id INT NOT NULL,
    ISBN VARCHAR(13) UNIQUE NOT NULL,
    Ano_publicacao INT,
    Genero_id INT NOT NULL,
    Editora_id INT NOT NULL,
    Quantidade_disponivel INT NOT NULL,
    Resumo TEXT,
    FOREIGN KEY (Autor_id) REFERENCES Autores(ID_autor),
    FOREIGN KEY (Genero_id) REFERENCES Generos(ID_genero),
    FOREIGN KEY (Editora_id) REFERENCES Editoras(ID_editora)
);

CREATE TABLE Usuarios (
    ID_usuario INT AUTO_INCREMENT PRIMARY KEY,
    Nome_usuario VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Senha_hash VARCHAR(255) NOT NULL,
    Numero_telefone VARCHAR(15),
    Data_inscricao DATE NOT NULL,
    Multa_atual DECIMAL(10, 2) NOT NULL DEFAULT(0)
);

CREATE TABLE Emprestimos (
    ID_emprestimo INT AUTO_INCREMENT PRIMARY KEY,
    Usuario_id INT NOT NULL,
    Livro_id INT NOT NULL,
    Data_emprestimo DATE NOT NULL,
    Data_devolucao_prevista DATE NOT NULL,
    Data_devolucao_real DATE,
    Status_emprestimo ENUM('pendente', 'devolvido', 'atrasado') NOT NULL,
    FOREIGN KEY (Usuario_id) REFERENCES Usuarios(ID_usuario),
    FOREIGN KEY (Livro_id) REFERENCES Livros(ID_livro)
);