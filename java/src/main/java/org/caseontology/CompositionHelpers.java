package org.caseontology;

import java.util.ArrayList;
import java.util.List;
import org.caseontology._case.investigation.InvestigativeAction;
import org.caseontology.uco.observable.ContentDataFacet;
import org.caseontology.uco.observable.FileFacet;
import org.caseontology.uco.observable.ObservableObject;
import org.caseontology.uco.observable.RasterPicture;
import org.caseontology.uco.observable.RasterPictureFacet;
import org.caseontology.uco.tool.Tool;
import org.caseontology.uco.types.Hash;

/** Fluent composition helpers derived from Composition Profiles. */
public final class CompositionHelpers {
    private CompositionHelpers() {}

    public static final class CsamEvidence {
        public final Tool tool;
        public final RasterPicture picture;
        public final InvestigativeAction action;

        public CsamEvidence(Tool tool, RasterPicture picture, InvestigativeAction action) {
            this.tool = tool;
            this.picture = picture;
            this.action = action;
        }
    }

    public static final class ToolRun {
        public final Tool tool;
        public final InvestigativeAction action;

        public ToolRun(Tool tool, InvestigativeAction action) {
            this.tool = tool;
            this.action = action;
        }
    }

    public static ObservableObject fileWithContentHashes(
            CaseGraph graph, String fileName, List<String[]> hashes) {
        FileFacet fileFacet = new FileFacet();
        fileFacet.getFileName().add(fileName);
        ContentDataFacet content = new ContentDataFacet();
        content.setHash(toHashes(hashes));
        ObservableObject obj = new ObservableObject();
        obj.getHasFacet().add(fileFacet);
        obj.getHasFacet().add(content);
        graph.add(obj);
        return obj;
    }

    public static RasterPicture rasterPictureWithHashes(
            CaseGraph graph, String fileName, List<String[]> hashes) {
        RasterPicture picture = new RasterPicture();
        FileFacet fileFacet = new FileFacet();
        fileFacet.getFileName().add(fileName);
        ContentDataFacet content = new ContentDataFacet();
        content.setHash(toHashes(hashes));
        picture.getHasFacet().add(fileFacet);
        picture.getHasFacet().add(content);
        picture.getHasFacet().add(new RasterPictureFacet());
        graph.add(picture);
        return picture;
    }

    public static CsamEvidence modelCsamEvidence(
            CaseGraph graph, String fileName, List<String[]> hashes) {
        return modelCsamEvidence(graph, fileName, hashes, "PhotoDNA", null);
    }

    public static CsamEvidence modelCsamEvidence(
            CaseGraph graph, String fileName, List<String[]> hashes,
            String hashingToolName, String hashingToolVersion) {
        Tool tool = new Tool();
        tool.setName(hashingToolName);
        tool.setVersion(hashingToolVersion);
        tool.setToolType("Content hashing");
        graph.add(tool);
        RasterPicture picture = rasterPictureWithHashes(graph, fileName, hashes);
        InvestigativeAction action = new InvestigativeAction();
        action.setName(hashingToolName + " hash of " + fileName);
        action.getInstrument().add(tool);
        action.getObject().add(picture);
        action.getResult().add(picture);
        graph.add(action);
        return new CsamEvidence(tool, picture, action);
    }

    public static ToolRun modelToolRun(
            CaseGraph graph, String toolName, String actionName, String toolVersion) {
        Tool tool = new Tool();
        tool.setName(toolName);
        tool.setVersion(toolVersion);
        graph.add(tool);
        InvestigativeAction action = new InvestigativeAction();
        action.setName(actionName);
        action.getInstrument().add(tool);
        graph.add(action);
        return new ToolRun(tool, action);
    }

    static List<Hash> toHashes(List<String[]> hashes) {
        List<Hash> list = new ArrayList<>();
        if (hashes == null) {
            return list;
        }
        for (String[] pair : hashes) {
            Hash h = new Hash();
            h.setHashMethod(pair[0]);
            h.setHashValue(hexToBytes(pair[1]));
            list.add(h);
        }
        return list;
    }

    static byte[] hexToBytes(String lexical) {
        if (lexical == null || lexical.isEmpty()) {
            return new byte[0];
        }
        String hex = lexical.trim();
        if (hex.startsWith("0x") || hex.startsWith("0X")) {
            hex = hex.substring(2);
        }
        if (hex.length() % 2 == 1) {
            hex = "0" + hex;
        }
        try {
            byte[] bytes = new byte[hex.length() / 2];
            for (int i = 0; i < bytes.length; i++) {
                bytes[i] = (byte) Integer.parseInt(hex.substring(i * 2, i * 2 + 2), 16);
            }
            return bytes;
        } catch (NumberFormatException ex) {
            return lexical.getBytes(java.nio.charset.StandardCharsets.UTF8);
        }
    }
}
