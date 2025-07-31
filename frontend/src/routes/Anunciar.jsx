import '../styles/Anunciar.css';
import { useState } from 'react';
import { Link } from 'react-router-dom';

export default function Anunciar() {
  const [foto, setFoto] = useState(null);

  const handleFotoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFoto(URL.createObjectURL(file));
    }
  };

  return (
    <div className="anunciar-page">
      <div className="upload-section">
        <div>
          <label className="upload-box">
            {foto ? (
              <img src={foto} alt="Preview" className="preview-image" />
            ) : (
              <span>Selecionar imagem do item</span>
            )}
            <input type="file" accept="image/*" onChange={handleFotoChange} hidden />
          </label>

          {/* ✅ Botão de voltar abaixo do upload */}
          <div style={{ marginTop: '20px', textAlign: 'center' }}>
            <Link to="/" className="btn-voltar"> Voltar para Doações</Link>
          </div>
        </div>
      </div>

      <div className="info-section">
        <h2>Anunciar Item</h2>
        <textarea placeholder="Descrição do item" rows={4} />
        <input type="text" placeholder="Endereço para retirada" />
        <button className="btn-localizacao">Usar localização atual</button>

        <input type="text" placeholder="Tempo de uso (ex: 2 anos)" />

        <select>
          <option value="">Estado do objeto</option>
          <option value="novo">Novo</option>
          <option value="semi-novo">Semi-novo</option>
          <option value="conservado">Conservado</option>
          <option value="desgastado">Desgastado</option>
          <option value="mal-funcionamento">Mal-funcionamento</option>
        </select>

        <select>
          <option value="">Classificação</option>
          <option value="tecnologia">Tecnologia</option>
          <option value="vestimenta">Vestimenta</option>
          <option value="objetos">Objetos</option>
          <option value="brinquedos">Brinquedos</option>
          <option value="automovel">Automóvel</option>
        </select>

        <input type="text" value="Disponível" disabled />

        <button className="btn-enviar">Anunciar</button>
      </div>
    </div>
  );
}
