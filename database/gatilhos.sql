DELIMITER //

CREATE TRIGGER
trg_repoe_livro AFTER UPDATE
ON emprestimos
FOR EACH ROW
BEGIN
  IF NEW.status_emprestimo = "devolvido" THEN
    UPDATE livros SET quantidade_disponivel = quantidade_disponivel + 1 WHERE id_livro = livro_id
  END IF
END //
