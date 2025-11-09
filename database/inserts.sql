INSERT INTO autores (nome_autor, nacionalidade, data_nascimento, biografia) VALUES
('George Orwell', 'Britânico', '1903-06-25', 'Autor conhecido por suas obras distópicas e críticas sociais.'),
('J.K. Rowling', 'Britânica', '1965-07-31', 'Criadora da famosa série Harry Potter.'),
('Gabriel García Márquez', 'Colombiano', '1927-03-06', 'Ganhador do Nobel de Literatura, mestre do realismo mágico.'),
('Machado de Assis', 'Brasileiro', '1839-06-21', 'Um dos maiores escritores brasileiros, fundador da Academia Brasileira de Letras.'),
('Haruki Murakami', 'Japonês', '1949-01-12', 'Autor contemporâneo conhecido por suas narrativas surreais e introspectivas.'),
('Jane Austen', 'Britânica', '1775-12-16', 'Escritora clássica inglesa, conhecida por obras sobre costumes e moral da sociedade.'),
('Stephen King', 'Americano', '1947-09-21', 'Mestre do terror e suspense, autor de dezenas de best-sellers.'),
('Clarice Lispector', 'Brasileira', '1920-12-10', 'Uma das mais importantes escritoras brasileiras do século XX.'),
('J.R.R. Tolkien', 'Britânico', '1892-01-03', 'Criador do universo de O Senhor dos Anéis e O Hobbit.'),
('Franz Kafka', 'Tcheco', '1883-07-03', 'Autor modernista conhecido por suas obras existencialistas e absurdas.');

INSERT INTO generos (nome_genero) VALUES
('Ficção Científica'),
('Fantasia'),
('Realismo Mágico'),
('Clássico'),
('Romance'),
('Terror'),
('Filosófico'),
('Drama'),
('Aventura'),
('Distopia');

INSERT INTO editoras (nome_editora, endereco_editora) VALUES
('Editora Aurora', 'Rua das Flores, 10, Centro'),
('Editora Horizonte', 'Av. Paulista, 1000, Bela Vista'),
('Editora Marítima', 'R. do Porto, 45, Bairro Alto'),
('Editora Verde', 'Travessa das Palmeiras, 7'),
('Editora Solar', 'Praça Central, 1, Sala 2'),
('Editora Luminosa', 'Av. das Nações, 200'),
('Editora Atlas', 'R. dos Navegantes, 88'),
('Editora Ponto e Vírgula', 'Alameda dos Livros, 12'),
('Editora Prisma', 'R. Nova, 150, 3º andar'),
('Editora Zênite', 'Av. Central, 100');

INSERT INTO livros (titulo, autor_id, isbn, ano_publicacao, genero_id, editora_id, quantidade_disponivel, resumo) VALUES
('1984', 1, '9780451524935', 1949, 10, 5, 12, 'Romance distópico sobre um regime totalitário que controla todos os aspectos da vida.'),
('Harry Potter e a Pedra Filosofal', 2, '9780747532699', 1997, 2, 2, 20, 'Primeiro livro da série Harry Potter, onde o jovem bruxo descobre seu destino.'),
('Cem Anos de Solidão', 3, '9780060883287', 1967, 3, 4, 15, 'Saga da família Buendía na mítica Macondo, mistura de fantasia e realidade.'),
('Dom Casmurro', 4, '9788520921086', 1899, 4, 3, 8, 'Clássico da literatura brasileira que aborda ciúme, dúvida e traição.'),
('Kafka à Beira-Mar', 5, '9788535912951', 2002, 7, 1, 10, 'Uma história surreal sobre destino, memórias e mundos paralelos.'),
('Orgulho e Preconceito', 6, '9780141439518', 1813, 5, 5, 9, 'Romance clássico sobre amor e convenções sociais na Inglaterra do século XIX.'),
('O Iluminado', 7, '9780307743657', 1977, 6, 7, 13, 'Um escritor enlouquece em um hotel isolado tomado por forças malignas.'),
('A Hora da Estrela', 8, '9788520920645', 1977, 8, 3, 11, 'A narrativa da vida de uma jovem nordestina pobre contada por um escritor em crise.'),
('O Senhor dos Anéis: A Sociedade do Anel', 9, '9780261102354', 1954, 9, 5, 18, 'Primeiro volume da épica jornada pela Terra-média em busca do Um Anel.'),
('A Metamorfose', 10, '9780140184780', 1915, 7, 10, 14, 'Um homem acorda transformado em um inseto e enfrenta o isolamento e a rejeição.');
