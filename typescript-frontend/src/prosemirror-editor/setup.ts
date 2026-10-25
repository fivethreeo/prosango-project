import { exampleSetup } from "prosemirror-example-setup";
import { Schema } from "prosemirror-model";
import { schema as basicSchema } from "prosemirror-schema-basic";
import { addListNodes } from "prosemirror-schema-list";
import { Plugin } from "prosemirror-state";
import { breadcrumbPlugin } from "../../prosemirror-breadcrumbs/src/index";

export const prosangoSchema = new Schema({
  nodes: addListNodes(basicSchema.spec.nodes, "paragraph block*", "block"),
  marks: basicSchema.spec.marks,
});

export function prosangoSrt(): Plugin[] {
  return [
    ...exampleSetup({ schema: prosangoSchema }),
    breadcrumbPlugin({ showMarks: true }),
  ];
}
