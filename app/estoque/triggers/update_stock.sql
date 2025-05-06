-- Trigger Function: atualiza_estoque
CREATE OR REPLACE FUNCTION atualiza_estoque()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.tipo = 'entrada' THEN
    -- Atualiza estoque no armazém de destino
    UPDATE produtos_estoque
    SET quantidade = quantidade + NEW.quantidade,
        atualizado_em = NOW()
    WHERE produto_id = NEW.produto_id AND armazem_id = NEW.armazem_destino_id;

  ELSIF NEW.tipo = 'saida' THEN
    -- Atualiza estoque no armazém de origem
    UPDATE produtos_estoque
    SET quantidade = quantidade - NEW.quantidade,
        atualizado_em = NOW()
    WHERE produto_id = NEW.produto_id AND armazem_id = NEW.armazem_origem_id;

  ELSIF NEW.tipo = 'ajuste' THEN
    -- Ajuste pode ser positivo ou negativo no destino
    UPDATE produtos_estoque
    SET quantidade = quantidade + NEW.quantidade,
        atualizado_em = NOW()
    WHERE produto_id = NEW.produto_id AND armazem_id = NEW.armazem_destino_id;

  ELSIF NEW.tipo = 'transferencia' THEN
    -- Diminui no armazém de origem
    UPDATE produtos_estoque
    SET quantidade = quantidade - NEW.quantidade,
        atualizado_em = NOW()
    WHERE produto_id = NEW.produto_id AND armazem_id = NEW.armazem_origem_id;

    -- Aumenta no armazém de destino
    UPDATE produtos_estoque
    SET quantidade = quantidade + NEW.quantidade,
        atualizado_em = NOW()
    WHERE produto_id = NEW.produto_id AND armazem_id = NEW.armazem_destino_id;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Cria o trigger na tabela de movimentações
DROP TRIGGER IF EXISTS trigger_at_
